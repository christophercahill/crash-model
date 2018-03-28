# -*- coding: utf-8 -*-
import os
import subprocess
import argparse
import yaml
import sys

DATA_FP = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)))) + '/data/'

# For this pipeline to run
# crash data needs to be under raw in the data directory given


def add_concern_args(config):
    concern_args = []

    if 'concern_files' not in config.keys():
        return None

    for concern_file in config['concern_files']:
        if 'name' not in concern_file.keys():
            sys.exit('Concern must have a name')
        concern_arg = concern_file['name'] + ','
        if 'filename' not in concern_file.keys():
            sys.exit('Concern file must be given')
        concern_arg += concern_file['filename'] + ','
        if 'latitude' in concern_file.keys() and concern_file['latitude']:
            concern_arg += concern_file['latitude']
        concern_arg += ','
        if 'longitude' in concern_file.keys() and concern_file['longitude']:
            concern_arg += concern_file['longitude']
        concern_arg += ','
        if 'time' in concern_file.keys() and concern_file['time']:
            concern_arg += concern_file['time']
        concern_args.append(concern_arg)

    return ' '.join(concern_args)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # Can give a config file
    parser.add_argument("-c", "--config", type=str,
                        help="Can give a different .yml config file")
    parser.add_argument("-s", "--startyear", type=str,
                        help="Can limit data to crashes this year or later")
    parser.add_argument("-e", "--endyear", type=str,
                        help="Can limit data to crashes this year or earlier")

    args = parser.parse_args()
    config_file = 'data/config.yml'
    if args.config:
        config_file = args.config
    start_year = None
    end_year = None
    if args.startyear:
        start_year = args.startyear
    if args.endyear:
        end_year = args.endyear

    with open(config_file) as f:
        config = yaml.safe_load(f)

    # City
    if 'city' not in config.keys() or config['city'] is None:
        sys.exit('City is required in config file')
    city = config['city']

    if 'datadir' in config.keys() and config['datadir']:
        DATA_FP = config['datadir']

    # This block handles any extra map info as we have in Boston
    extra_map = None
    additional_features = None
    extra_map3857 = None
    recreate = False
    outputdir = city.split(',')[0]
    if 'extra_map' in config.keys() and config['extra_map']:
        # Require additional features and additional shapefile in 3857 proj
        if 'additional_features' not in config.keys() \
           or config['additional_features'] is None \
           or 'extra_map3857' not in config.keys() \
           or config['extra_map3857'] is None:
            sys.exit("If extra_map is given, additional_features and" +
                     "extra_map3857 are required.")
            
        extra_map = config['extra_map']
        additional_features = config['additional_features'].split()
        extra_map3857 = config['extra_map3857']

    # Latitude and longitude and time columns might be different
    # for different cities
    longitude_crash = None
    latitude_crash = None
    date_col_crash = None
    crash_files = None
    if 'crashfiles' in config.keys() and config['crashfiles']:
        crash_files = config['crashfiles']
    if 'longitude_crash' in config.keys() and config['longitude_crash']:
        longitude_crash = config['longitude_crash']
    if 'latitude_crash' in config.keys() and config['latitude_crash']:
        latitude_crash = config['latitude_crash']
    if 'date_col_crash' in config.keys() and config['date_col_crash']:
        date_col_crash = config['date_col_crash']

    # Handle any concern data here
    concern_args = add_concern_args(config)

    # Whether to regenerate maps from open street map
    if 'recreate' in config.keys() and config['recreate']:
        recreate = True

    # Features drawn from open street maps
    # additional_features from config file can add on to
    # But additional features are only added if you're using an extra map
    # beyond open street map
    features = [
        'width', 'lanes', 'hwy_type', 'osm_speed', 'signal', 'oneway']

    print "Generating maps for " + city + ' in ' + DATA_FP
    if recreate:
        print "Overwriting existing data..."
    # Get the maps out of open street map, both projections
    subprocess.check_call([
        'python',
        '-m',
        'data.osm_create_maps',
        city,
        DATA_FP,
    ] + (['--forceupdate'] if recreate else []))

    # Create segments on the open street map data
    subprocess.check_call([
        'python',
        '-m',
        'data.create_segments',
        '-d',
        DATA_FP,
        '-r',
        os.path.join(DATA_FP, 'processed/maps/osm_ways_3857.shp'),
        '-i',
        os.path.join(DATA_FP, 'processed/maps/osm_nodes.shp')
    ])

    if extra_map:
        # Extract intersections from the new city file
        # Write to a subdirectory so files created from osm aren't overwritten
        # Eventually, directory of additional files should also be an argument
        subprocess.check_call([
            'python',
            '-m',
            'data.extract_intersections',
            os.path.join(extra_map),
            '-d',
            DATA_FP,
            '-n',
            outputdir
        ] + (['--forceupdate'] if recreate else []))
        # Create segments from the Boston data
        subprocess.check_call([
            'python',
            '-m',
            'data.create_segments',
            '-d',
            DATA_FP,
            '-n',
            outputdir,
            '-r',
            extra_map3857
        ])

        # Map the boston segments to the open street map segments
        # and add features
        subprocess.check_call([
            'python',
            '-m',
            'data.add_map',
            DATA_FP,
            outputdir,
        ])

    subprocess.check_call([
        'python',
        '-m',
        'data.join_segments_crash_concern',
        '-d',
        DATA_FP
    ]
        + (['-crash'] + (crash_files if crash_files else []))
        + (['-x_crash', longitude_crash] if longitude_crash else [])
        + (['-y_crash', latitude_crash] if latitude_crash else [])
        + (['-t_crash', date_col_crash] if date_col_crash else [])
        + (['-start', start_year] if start_year else [])
        + (['-end', end_year] if end_year else [])
        + (['--concern', concern_args] if concern_args else [])
    )

    subprocess.check_call([
        'python',
        '-m',
        'data.ATR_scraping.geocode_snap_ATRs',
        '-d',
        DATA_FP
    ] + (['--forceupdate'] if recreate else []))
    subprocess.check_call([
        'python',
        '-m',
        'data.TMC_scraping.parse_tmc',
        '-d',
        DATA_FP
    ] + (['--forceupdate'] if recreate else []))

    if additional_features:
        features = features + additional_features

    # Throw in make canonical dataset here too just to keep track
    # of standardized features
    subprocess.check_call([
        'python',
        '-m',
        'features.make_canon_dataset',
        '-d',
        DATA_FP,
        '-features'
    ] + features
        + (['-t_crash', date_col_crash] if date_col_crash else [])
        + (['--concern', concern_args] if concern_args else []))
