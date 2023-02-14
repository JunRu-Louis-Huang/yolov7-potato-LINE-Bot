import os

# Imports the Google Cloud client library
from google.cloud import storage

YOUR_SERVICE = 'gcpai_janyu.json'  # gcpai_janyu.json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = YOUR_SERVICE
bucket_name = "janeai-10" # louisai # janeai-10

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(f"{destination_blob_name} with contents byte encode uploaded to {bucket_name}.")