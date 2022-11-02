import argparse
import time
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import cv2
import yaml
from torchvision import transforms
import numpy as np

from utils.datasets import letterbox
from utils.general_mask import non_max_suppression_mask_conf, increment_path
from utils.torch_utils import time_synchronized

from detectron2.modeling.poolers import ROIPooler
from detectron2.structures import Boxes
from detectron2.utils.memory import retry_if_cuda_oom
from detectron2.layers import paste_masks_in_image

def detectionProcess(image):
    image = letterbox(image, opt.img_size, stride=64, auto=True)[0]
    image_ = image.copy()
    image = transforms.ToTensor()(image)
    image = torch.tensor(np.array([image.numpy()]))
    image = image.to(device)
    image = image.half() if half else image.float()        

    t1 = time_synchronized()                
    output = model(image)
    t2 = time_synchronized()

    inf_out, train_out, attn, mask_iou, bases, sem_output = output['test'], output['bbox_and_cls'], output['attn'], output['mask_iou'], output['bases'], output['sem']

    bases = torch.cat([bases, sem_output], dim=1)

    nb, _, height, width = image.shape

    names = model.names

    pooler_scale = model.pooler_scale

    pooler = ROIPooler(output_size=hyp['mask_resolution'], scales=(pooler_scale,), sampling_ratio=1, pooler_type='ROIAlignV2', canonical_level=2)

    # NMS
    output, output_mask, output_mask_score, output_ac, output_ab = non_max_suppression_mask_conf(inf_out, attn, bases, pooler, hyp, opt.conf_thres, opt.iou_thres, merge=False, mask_iou=None)

    pred, pred_masks = output[0], output_mask[0]
    base = bases[0]

    image_result = None    

    if pred is not None:
        bboxes = Boxes(pred[:, :4])
        original_pred_masks = pred_masks.view(-1, hyp['mask_resolution'], hyp['mask_resolution'])

        pred_masks = retry_if_cuda_oom(paste_masks_in_image)( original_pred_masks, bboxes, (height, width), threshold=0.5)

        pred_masks_np = pred_masks.detach().cpu().numpy()
        pred_cls = pred[:, 5].detach().cpu().numpy()
        pred_conf = pred[:, 4].detach().cpu().numpy()
        nbboxes = bboxes.tensor.detach().cpu().numpy().astype(int)

        image_result = image[0].permute(1, 2, 0)*255
        image_result = image_result.cpu().numpy().astype(np.uint8)

        image_result = cv2.cvtColor(image_result, cv2.COLOR_RGB2BGR)

        for one_mask, bbox, cls, conf in zip(pred_masks_np, nbboxes, pred_cls, pred_conf):
            if conf < 0.25:
                continue

            color = [np.random.randint(255), np.random.randint(255), np.random.randint(255)]                                
                                
            image_result[one_mask] = image_result[one_mask] * 0.5 + np.array(color, dtype=np.uint8) * 0.5
            image_result = cv2.rectangle(image_result, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            label = '%s %.3f' % (names[int(cls)], conf)
            t_size = cv2.getTextSize(label, 0, fontScale=0.5, thickness=1)[0]
            c2 = bbox[0] + t_size[0], bbox[1] - t_size[1] - 3

            image_result = cv2.rectangle(image_result, (bbox[0], bbox[1]), c2, color, -1, cv2.LINE_AA)  # filled
            image_result = cv2.putText(image_result, label, (bbox[0], bbox[1] - 2), 0, 0.5, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)                

        print(f'Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference')

    return image_result

def imageSource(save_path):
    image = cv2.imread(opt.source)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_size = image.shape

    image_result = detectionProcess(image)

    image_result = cv2.resize(image_result, (image_size[1], image_size[0]))

    # Show Result
    if opt.view_img:
        cv2.imshow("Detection Result", image_result)
        cv2.waitKey(0)
    
    # Save Result
    cv2.imwrite(save_path, image_result)
    print("Result saved : ", save_path)


def videoSource(save_path, webcam):
    if webcam:
        cap = cv2.VideoCapture(int(opt.source))
    else:
        cap = cv2.VideoCapture(opt.source)
    
    (grabbed, frame) = cap.read()

    fps_source = cap.get(cv2.CAP_PROP_FPS)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 1

    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps_source, (w, h), True)

    while(grabbed):                
        image = frame.copy()
        print("{}{}/{})".format("\nFrame (", current_frame, total_frame))
        image_result = detectionProcess(image)

        # Show Result
        if opt.view_img or webcam:
            cv2.imshow("Detected", image_result)            

        # Save Result
        image_result = cv2.resize(image_result, (w, h))
        vid_writer.write(image_result)

        if cv2.waitKey(1) == ord('q'):
            break
        
        (grabbed, frame) = cap.read()
        current_frame += 1        

def detect(opt):
    webcam = opt.source.isnumeric()

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    save_dir.mkdir(parents=True, exist_ok=True)  # make dir

    extension = opt.source.split('.')[-1].lower()
    image_name = "result."+extension

    save_path = str(save_dir / image_name)

    if webcam:
        save_path = str(save_dir / opt.source)
        save_path = save_path + ".mp4"

    img_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']

    if extension in img_formats:
        imageSource(save_path)
    else:
        videoSource(save_path, webcam)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='yolov7-mask.pt', help='model.pt path(s)')
    parser.add_argument('--hyp', type=str, default='data/hyp.scratch.mask.yaml', help='Hyperparameter')
    parser.add_argument('--source', type=str, default='inference/images/bus.jpg', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)    

    with torch.no_grad():
        # Device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if(device.type != 'cpu'):
            compute_capability = torch.cuda.get_device_capability(device=device)    
            half = (device.type != 'cpu') and (compute_capability[0] >= 8)  # half precision only supported on CUDA

        # Load Model
        weights = torch.load(opt.weights)
        model = weights['model'].to(device)

        with open(opt.hyp) as f:
            hyp = yaml.load(f, Loader=yaml.FullLoader)
        
        model = model.half() if half else model.float()            

        detect(opt=opt)