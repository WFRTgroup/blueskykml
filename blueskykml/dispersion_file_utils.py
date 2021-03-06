# TODO: refactor this as a class (possibly singleton?) that takes config in contstructor

import os

from .constants import *
from .memoize import memoizeme

__all__ = [
    'create_dispersion_images_dir', 'create_image_set_dir',
    'image_pathname', 'legend_pathname', 'parse_color_map_names',
    'collect_all_dispersion_images', 'collect_dispersion_images'
]

def create_height_label(height):
    """Doesn't do much, but it's centralized so that we change easily
    """
    if height == "column_integrated":
        return height

    return height + 'm'

def create_dir_if_does_not_exist(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

def create_dispersion_images_dir(config):
    outdir = config.get('DispersionGridOutput', "OUTPUT_DIR")
    create_dir_if_does_not_exist(outdir)

def create_polygon_kmls_dir(config):
    outdir = config.get('PolygonsKML', "POLYGONS_OUTPUT_DIR")
    create_dir_if_does_not_exist(outdir)

def create_image_set_dir(config, *dirs):
    """Creates the directory to contain the specified image set, if necessary"""
    images_output_dir = config.get('DispersionGridOutput', "OUTPUT_DIR")
    dirs = [str(d) for d in dirs]
    outdir = os.path.join(images_output_dir, *dirs)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    return outdir

def image_pathname(image_set_dir, height_label, time_series_type, ts,
        utc_offset=None):
    filename = ts.strftime(height_label + '_'
        + IMAGE_PREFIXES[time_series_type]
        + FILE_NAME_TIME_STAMP_PATTERNS[time_series_type])
    if utc_offset is not None:
        filename += '_' + get_utc_label(utc_offset)
    return os.path.join(image_set_dir, filename)

def legend_pathname(image_set_dir, height_label, time_series_type,
        utc_offset=None):
    filename = "%s_colorbar_%s" % (height_label,
        TIME_SET_DIR_NAMES[time_series_type])
    if utc_offset is not None:
        filename += '_' + get_utc_label(utc_offset)
    return os.path.join(image_set_dir, filename)

def get_utc_label(utc_offset):
    return 'UTC{}{}{}00'.format('+' if utc_offset >= 0 else '-',
        '0' if abs(utc_offset) < 10 else '', abs(utc_offset))


# TODO: parse_color_map_names belongs somewhere else...or maybe this module,
# dispersion_file_utils, should be renamed more generically
# Note: this will memoize for a single instance of the config parse
# TODO: pass in color map names string instead of the config object ?
@memoizeme
def parse_color_map_names(config, set_name):
    if config.has_option("DispersionGridOutput", set_name):
        return [name.strip() for name in config.get("DispersionGridOutput", set_name).split(',')]
    return []

def is_smoke_image(file_name, height_label, time_series_type):
    return (file_name.startswith(height_label + '_'
        + IMAGE_PREFIXES[time_series_type]))


##
## Collecting all images for post-processing
##

@memoizeme
def collect_all_dispersion_images(config, heights):
    """Collect images from all sets of colormap images in each time series
    category
    """
    images = {}

    for height in heights:
        height_label = create_height_label(height)
        images[height_label] = dict((v, {}) for v in TimeSeriesTypes.ALL)
        for time_series_type in TimeSeriesTypes.ALL:
            if time_series_type in (TimeSeriesTypes.DAILY_MAXIMUM,
                    TimeSeriesTypes.DAILY_AVERAGE):
                utc_offsets = config.get('DispersionImages',
                    "DAILY_IMAGES_UTC_OFFSETS")
                for utc_offset in utc_offsets:
                    collect_all_colormap_dispersion_images(config, images,
                        height_label, time_series_type, utc_offset=utc_offset)
            else:
                collect_all_colormap_dispersion_images(config, images,
                    height_label, time_series_type)
    return images

def collect_all_colormap_dispersion_images(config, images, height_label,
        time_series_type, utc_offset=None):
    keys = [height_label, TIME_SET_DIR_NAMES[time_series_type]]
    if utc_offset is not None:
        keys.append(get_utc_label(utc_offset))

    for color_map_section in parse_color_map_names(config,
            CONFIG_COLOR_LABELS[time_series_type]):
        # Initialize and get reference to nested color section imatges dict
        _keys = keys + [color_map_section]
        color_set = initialize_sections_dict(images, *_keys)

        # create output dir
        color_set['root_dir'] = create_image_set_dir(config, *_keys)

        # collect images
        for image in os.listdir(color_set['root_dir']):
            if is_smoke_image(image, height_label, time_series_type):  # <-- this is to exclude color bar
                color_set['smoke_images'].append(image)
            else:  #  There should only be smoke images and a legend
                color_set['legend'] = image


##
## Collection images for KML
##

# Note: collect_dispersion_images_for_kml was copied over from
# smokedispersionkml.py and refactored to remove redundancy
def collect_dispersion_images_for_kml(config, heights):
    """Collect images from first set of colormap images in each time series
    category. Used in KML generation.
    """
    images = {}

    for height in heights:
        height_label = create_height_label(height)
        for time_series_type in TimeSeriesTypes.ALL:
            if time_series_type in (TimeSeriesTypes.DAILY_MAXIMUM,
                    TimeSeriesTypes.DAILY_AVERAGE):
                utc_offsets = config.get('DispersionImages',
                    "DAILY_IMAGES_UTC_OFFSETS")
                for utc_offset in utc_offsets:
                    collect_color_map_dispersion_images_section_for_kml(
                        config, images, height_label, time_series_type,
                        utc_offset)
            else:
                collect_color_map_dispersion_images_section_for_kml(
                    config, images, height_label, time_series_type)
    return images

def collect_color_map_dispersion_images_section_for_kml(config, images,
        height_label, time_series_type, utc_offset=None):
    color_map_sections = parse_color_map_names(config,
        CONFIG_COLOR_LABELS[time_series_type])
    if color_map_sections and len(color_map_sections) > 0:
        # Initialize and get reference to nested color section imatges dict
        keys = [height_label, time_series_type]
        if utc_offset is not None:
            keys.append(get_utc_label(utc_offset))
        images_section = initialize_sections_dict(images, *keys)

        # create output dir
        keys[1] = TIME_SET_DIR_NAMES[keys[1]]
        keys.append(color_map_sections[0])
        outdir = create_image_set_dir(config, *keys)

        # collect images
        images_section['root_dir'] = outdir
        for image in os.listdir(outdir):
            if is_smoke_image(image, height_label, time_series_type):  # <-- this is to exclude color bar
                images_section['smoke_images'].append(image)
            else:  #  There should only be smoke images and a legend
                images_section['legend'] = image

##
## General image collecting utilities
##

def initialize_sections_dict(images, *keys):
    if len(keys) > 1:
        images[keys[0]] = images.get(keys[0], {})
        return initialize_sections_dict(images[keys[0]], *keys[1:])
    else:
        images[keys[0]] = images.get(keys[0], {'smoke_images':[], 'legend': None})
        return images[keys[0]]
