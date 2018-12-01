
import os
import glob
import yaml

from datetime import datetime
from multiprocessing import Pool
from functools import partial

from ProcessImage import ProcessImage
from geopy.geocoders import Nominatim, GoogleV3

IMAGE_FOLDER = './_TestData/'
OUTPUT_FOLDER = '_Output'

CONFIG_FILE = 'config.yml'

EXTENSIONS = ['.jpg', '.jpeg']

USE_GOOGLE_API = False
MULTI_PROCESSING = True

USER_AGENT = 'Photos'


def load_config(config_file):
    """Load Config."""
    if not USE_GOOGLE_API:
        return {'google_api_key': ''}

    if not os.path.isfile(config_file):
            raise ValueError("Configuration file {0} not found.".format(config_file))

    with open(config_file, 'r') as ymlfile:
        return yaml.load(ymlfile)


def multi_processing(images, geolocator):
    pool = Pool(os.cpu_count())
    pool.map(partial(ProcessImage,
                     geolocator=geolocator,
                     output_folder=OUTPUT_FOLDER,
                     use_google_api=USE_GOOGLE_API), images)

def single_processing(images, geolocator):
    for image in images:
        ProcessImage(image, geolocator, OUTPUT_FOLDER, USE_GOOGLE_API)

def main():
    """Main."""
    start_time = datetime.now().replace(microsecond=0)
    cfg = load_config(CONFIG_FILE)

    if USE_GOOGLE_API:
        geolocator = GoogleV3(user_agent=USER_AGENT, api_key=cfg['google_api_key'])
    else:
        geolocator = Nominatim(user_agent=USER_AGENT)

    if not os.path.isdir(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    images = []
    for root, _dirs, files in os.walk(IMAGE_FOLDER):
        for file in files:
            if file.lower().endswith(tuple(EXTENSIONS)):
                images.append(os.path.join(root, file))

    if MULTI_PROCESSING:
        multi_processing(images, geolocator)
    else:
        single_processing(images, geolocator)

    end_time = datetime.now().replace(microsecond=0)
    print("Processing {0} Images in {1} seconds.".format(len(images), str(end_time - start_time)))


if __name__ == '__main__':
    main()
