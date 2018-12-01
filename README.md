
# Print Photo EXIF Information

Prints photos with location and EXIF data.

EXIF GPS location information is resolved by OpenStreetMap (default) or Google Geocoding API.

## References

- <https://python-xmp-toolkit.readthedocs.io/en/latest/>
- <https://libopenraw.freedesktop.org/wiki/Exempi/>
- <https://www.oclc.org/developer/news/2016/making-sense-of-linked-data-with-python.en.html>
- <https://www.tutorialspoint.com/python3/python_xml_processing.htm>
- <https://forums.adobe.com/thread/1529360>
- <https://github.com/drewsberry/gpsextract>
- <https://gist.github.com/snakeye/fdc372dbf11370fe29eb>
- <https://developers.google.com/maps/documentation/geocoding/start>
- <https://github.com/geopy/geopy>
- <https://chrisalbon.com/python/data_wrangling/geocoding_and_reverse_geocoding/>

## Setup Python Virtual Environment

~~~
python3 -m venv venv
~~~

## Active Python Virtual Environment

~~~
.  ./venv/bin/activate
~~~

## Install Dependencies

~~~
brew install Exempi
~~~

## Install Requirements

~~~
pip install -r requirements.txt
~~~

## Configuration

Place images in the ```_TestData``` folder (sub-folders supported) and convert iPhone HEIC files to JPEG if needed.

### Google API, if used

<https://developers.google.com/maps/documentation/geocoding/get-api-key>

Create file ```config.yml``` with the following contain: -

~~~
---
google_api_key: "<GOOGLE_API_KEY>"
~~~

> Where ```<GOOGLE_API_KEY>``` is replaced with your Google API Key.
> Set ```USE_GOOGLE_API``` to ```True``` in script ```print_exif_info.py``` to use it.

## Run

~~~
python print_exif_info.py
~~~

## Profiling

~~~
python -m cProfile -s tottime print_exif_info.py | tee profile.log
~~~

## Deactivate Python Virtual Environment

~~~
deactivate
~~~
