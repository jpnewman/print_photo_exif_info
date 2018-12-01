import exifread

from mezmorize import Cache


CACHE = Cache(CACHE_TYPE='filesystem', CACHE_DIR='cache')


# https://github.com/drewsberry/gpsextract/blob/master/gpsread.py
def ratio_to_float(ratio):
    """ratio_to_float."""
    # Takes exif tag value ratio as input and outputs float

    if not isinstance(ratio, exifread.utils.Ratio):
        raise ValueError("You passed something to ratio_to_float that isn't "
                         "a GPS ratio.")

    # GPS metadata is given as a number and a density
    return ratio.num / ratio.den


# https://github.com/drewsberry/gpsextract/blob/master/gpsread.py
def tag_to_float(gps_tag):
    """tag_to_float."""
    # Takes GPS exif lat or long tag as input and outputs as simple float in
    # degrees

    if gps_tag is None:
        return None

    if not isinstance(gps_tag, exifread.classes.IfdTag):
        raise ValueError("You passed something to tag_to_float that isn't an "
                         "EXIF tag.")

    _gps_ang = [ratio_to_float(ratio) for ratio in gps_tag.values]

    _gps_float = _gps_ang[0] + _gps_ang[1] / 60 + _gps_ang[2] / 3600

    return _gps_float


# https://programminghistorian.org/en/lessons/transliterating
cyrillic_translit = {
    u'\u0410': 'A', u'\u0430': 'a',
    u'\u0411': 'B', u'\u0431': 'b',
    u'\u010d': 'C', 
    u'\u0412': 'V', u'\u0432': 'v',
    u'\u0413': 'G', u'\u0433': 'g',
    u'\u0414': 'D', u'\u0434': 'd',
    u'\u0415': 'E', u'\u0435': 'e',
    u'\u0416': 'Zh', u'\u0436': 'zh',
    u'\u0417': 'Z', u'\u0437': 'z',
    u'\u0418': 'I', u'\u0438': 'i',
    u'\u0419': 'I', u'\u0439': 'i',
    u'\u041a': 'K', u'\u043a': 'k',
    u'\u041b': 'L', u'\u043b': 'l',
    u'\u041c': 'M', u'\u043c': 'm',
    u'\u041d': 'N', u'\u043d': 'n',
    u'\u041e': 'O', u'\u043e': 'o',
    u'\u00f3': 'o',
    u'\u041f': 'P', u'\u043f': 'p',
    u'\u0420': 'R', u'\u0440': 'r',
    u'\u0421': 'S', u'\u0441': 's',
    u'\u0422': 'T', u'\u0442': 't',
    u'\u0423': 'U', u'\u0443': 'u',
    u'\u0424': 'F', u'\u0444': 'f',
    u'\u0425': 'Kh', u'\u0445': 'kh',
    u'\u0426': 'Ts', u'\u0446': 'ts',
    u'\u0427': 'Ch', u'\u0447': 'ch',
    u'\u0428': 'Sh', u'\u0448': 'sh',
    u'\u0429': 'Shch', u'\u0449': 'shch',
    u'\u042a': '"', u'\u044a': '"',
    u'\u042b': 'Y', u'\u044b': 'y',
    u'\u042c': "'", u'\u044c': "'",
    u'\u042d': 'E', u'\u044d': 'e',
    u'\u042e': 'Iu', u'\u044e': 'iu',
    u'\u042f': 'Ia', u'\u044f': 'ia',
    u'\u017e': 'z',
    u'\u00ed': 'i',
    u'\u00e1': 'a',
    u'\u00e3': 'a',
    u'\u00f1': 'n'
}


# https://programminghistorian.org/en/lessons/transliterating
def transliterate(word, translit_table):
    converted_word = ''
    for char in word:
        transchar = ''
        if char in translit_table:
            transchar = translit_table[char]
        else:
            transchar = char
        converted_word += transchar
    return converted_word


@CACHE.memoize()
def get_location_from_lat_lon(geolocator, lat, lon, timeout=25):
    """get_location_from_lat_lon."""
    location = geolocator.reverse("{0}, {1}".format(lat, lon), timeout=timeout)
    return location
