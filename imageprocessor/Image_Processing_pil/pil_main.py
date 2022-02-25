import logging
import os
import glob
import PIL.Image
from google.cloud import storage
from PIL import Image

logging.basicConfig(filename="../test.log", format='%(levelname)s : %(message)s', level=logging.DEBUG)
#ToDo: create a global client

def download_files_gcp(bucket):
    logging.info("downloading started")
    storage_client = storage.Client.from_service_account_json("/Users/nivedita/Documents/codebases/configs/airasia"
                                                              "-hotelsbe-dev.json")
    bucket = storage_client.get_bucket(bucket)
    blobs = bucket.list_blobs(prefix="image_processing_demo_bucket/test_images")
    for blob in blobs:
        filename = blob.name.replace('/', '_')
        blob.download_to_filename("data/" + filename)


def image_file_processing(filepath, quality, width, height):
    logging.info("image processing started")
    resize_dir = filepath + "/resized"
    if not os.path.exists(resize_dir):
        os.makedirs(resize_dir)
    files = os.listdir(filepath)
    images = [file for file in files if file.endswith(('jpg', 'png', 'jpeg'))]
    for imgname in images:
        logging.info("resizing file " + imgname)
        img = Image.open(filepath + "/" + imgname)
        if width is None and height is None:
            logging.info("width and height is not given of the images")
            width, height = img.size
            logging.info("getting info from image width: {}, height: {}".format(width, height))
        img = img.resize((width, height), PIL.Image.BICUBIC)
        img.save(filepath + "/resized/" + imgname, optimize=True, quality=quality)
        logging.info(f"resized images are stored in {resize_dir}")
    return resize_dir


def upload_to_cloud(filepath, dest_bucket_name, dest_blob_name):
    # ToDo: delete the files after uploading check if the files are deleted or not and log it
    logging.info("uploading started")
    GCS_CLIENT = storage.Client.from_service_account_json("/Users/nivedita/Documents/codebases/configs/airasia"
                                                              "-hotelsbe-dev.json")
    rel_paths = glob.glob(filepath + '/**', recursive=True)
    logging.info(f"uploading data from {rel_paths}")
    bucket = GCS_CLIENT.get_bucket(dest_bucket_name)
    for local_file in rel_paths:
        remote_path = f'{dest_blob_name}/{"/".join(local_file.split(os.sep)[1:])}'
        if os.path.isfile(local_file):
            blob = bucket.blob(remote_path)
            logging.info(f"uploading file from local {local_file} remote {remote_path}")
            blob.upload_from_filename(local_file)
    logging.info("uploading files completed")


if __name__ == '__main__':
    # resize = image_file_processing('/Users/nivedita/Documents/images_test', quality=65, width=None, height=None)
    download_files_gcp('image_processing_demo_bucket')
