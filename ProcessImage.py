import os

from exifread import process_file
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


from helpers import tag_to_float, get_location_from_lat_lon, transliterate, cyrillic_translit


class ProcessImage():
    """Process Images Class"""

    def __init__(self, filename, geolocator, output_folder, use_google_api):
        """Init."""
        self.filename = filename
        self.geolocator = geolocator
        self.output_folder = output_folder

        self.use_google_api = use_google_api

        # EXIF
        self.lat = None
        self.lat_ref = None
        self.lon = None
        self.lon_ref = None
        self.date_time = None
        self.exif_date_time = None
        self.orientation = None

        self.title = ""
        self.margin = 10

        self.location = None

        self.process()


    def get_exif(self):
        """Get EXIF."""
        f = open(self.filename, 'rb')
        tags = process_file(f)

        for tag in tags.keys():
            if tag == 'GPS GPSLatitude':
                self.lat = tags[tag]
            elif tag == 'GPS GPSLatitudeRef':
                self.lat_ref = tags[tag]
            elif tag == 'GPS GPSLongitude':
                self.lon = tags[tag]
            elif tag == 'GPS GPSLongitudeRef':
                self.lon_ref = tags[tag]
            elif tag == 'Image DateTime':
                self.date_time = tags[tag]
            elif tag == 'EXIF DateTimeOriginal':
                self.exif_date_time = tags[tag]
            elif tag == 'Image Orientation':
                self.orientation = tags[tag].values[0]

        self.lat = tag_to_float(self.lat)
        self.lon = tag_to_float(self.lon)

        if self.lat is not None and self.lat_ref.values != 'N':
            self.lat = 0 - self.lat

        if self.lon is not None and self.lon_ref.values != 'E':
            self.lon = 0 - self.lon

        if self.date_time is None and self.exif_date_time is not None:
            self.date_time = self.exif_date_time.values
        elif self.date_time is not None:
            self.date_time = self.date_time.values

    def set_google_title(self):
        # TODO: Parse Google API location output.
        self.title = self.location[0].address

    def set_open_street_map_title(self):
        location_area_text = ''

        if 'city' in self.location.raw['address']:
            location_area_text = self.location.raw['address']['city']
        elif 'county' in self.location.raw['address']:
            location_area_text = self.location.raw['address']['county']

        if location_area_text != '':
            location_area_text += ', '

        country = self.location.raw['address']['country'].split('/')[-1]
        self.title = "{0}{1}".format(location_area_text, country)


    def set_title_from_location(self):
        if self.use_google_api:
            self.set_google_title()
        else:
            self.set_open_street_map_title()

    def write_image_text(self, img_draw, font, text, img_w, text_width, text_y_pos, right_align=False):
        """write image text."""
        y_pos = text_y_pos - self.margin
        pos = (self.margin, y_pos)
        if right_align:
            pos = (img_w - text_width - self.margin, y_pos)

        img_draw.text(pos, text, font=font, fill=(255, 32, 0))


    def write_info_line(self, img, img_w, img_h, font_size=25):
        """write info line."""
        fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', font_size)
        draw = ImageDraw.Draw(img)

        line_dimensions = [draw.textsize(t, font=fnt) for t in [self.title, self.date_time]]
        text_y_pos = (img_h - max(h for w, h in line_dimensions))

        self.write_image_text(draw, fnt, self.title,
                              img_w, line_dimensions[0][0], text_y_pos)
        self.write_image_text(draw, fnt, self.date_time,
                              img_w, line_dimensions[1][0], text_y_pos,
                              right_align=True)


    def save_image(self, im, original_filename):
        """save image."""
        out_filetitle_title = self.title.replace(' ', '_').replace(',', '')
        out_filetitle_date_time = self.date_time.replace(':', '-')
        out_filetitle = "{0}-{1}_{2}.jpg".format(out_filetitle_title,
                                                 out_filetitle_date_time,
                                                 original_filename).replace(' ', '_').replace('/', '-')
        out_filename = os.path.join(self.output_folder, out_filetitle)
        out_filename_transliterated = transliterate(out_filename, cyrillic_translit)

        # print(out_filename_transliterated)
        im.save(out_filename_transliterated)


    def write_image(self):
        """write image."""
        desired_width = 1800
        desired_height = 1200

        im = Image.open(self.filename)
        w, h = im.size

        if self.orientation == 3:
            im = im.rotate(180, expand=True)

        new_height = 1200
        height_percent = (new_height / float(h))
        new_width = int((float(w) * float(height_percent)))

        # Resize
        im.thumbnail((new_width, new_height), Image.ANTIALIAS)

        # Write Info
        self.write_info_line(im, new_width, new_height)

        # Resize
        new_im = Image.new("RGB", (desired_width, desired_height), color=(255, 255, 255, 0))
        new_im.paste(im, ((desired_width - new_width) // 2,
                          (desired_height - new_height) // 2))

        file_path = os.path.split(self.filename)[1]
        file_title = os.path.splitext(file_path)[0]
        self.save_image(new_im, file_title)

        # im.show()

    def process(self):
        """Process."""
        print(self.filename)

        self.get_exif()

        if self.lat is None or self.lon is None:
            print("WARNING: Not GPS Exif data: {0}".format(self.filename))
            return

        self.location = get_location_from_lat_lon(self.geolocator, self.lat, self.lon)

        if self.location is None:
            return

        self.set_title_from_location()

        self.write_image()
