# importing lib
import os
import glob
import logging
import cv2
import imutils as im
from google.cloud import storage

logging.basicConfig(filename="../test.log", format='%(levelname)s : %(message)s', level=logging.DEBUG)


# ToDo: create a global client

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
    global new_w, new_h
    logging.info("image processing started")
    resize_dir = filepath + "/resized_open"
    if not os.path.exists(resize_dir):
        os.makedirs(resize_dir)
    files = os.listdir(filepath)
    images = [file for file in files if file.endswith(('jpg', 'png', 'jpeg'))]
    for imgname in images:
        logging.info("resizing file " + imgname)
        img = cv2.imread(filepath + "/" + imgname, cv2.IMREAD_UNCHANGED)
        width, height = (None, None)
        if width is None and height is None:
            logging.info("width and height is not given of the images")
            width, height = (img.shape[1], img.shape[0])
            if width is not None and height is not None:
                logging.info("getting info from image width: {}, height: {}".format(width, height))
                new_h = int(height * quality)
                new_w = int(width * quality)
                logging.info("getting info from new dim width: {}, height: {}".format(new_w, new_h))
        reimg = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(resize_dir+'/'+imgname.replace('test', 'resized'), reimg)
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
    resize = image_file_processing('/Users/nivedita/Documents/images_test/images', quality=0.6, width=None, height=None)
    # download_files_gcp('image_processing_demo_bucket')
