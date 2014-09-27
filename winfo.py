#!/usr/bin/env python2

import urllib2      # for fetching weather data
import json         # for parsing weather data
import re           # for parsing the format string
import argparse     # for parsing CLI args
import os.path      # for getting the path to the profiles

# Current version information
PROGRAM_NAME = 'winfo'
MAJOR_VERSION = '0'
MINOR_VERSION = '3'
COPYRIGHT = 'Copyright (c) 2014 Brian Kubisiak <velentr.rc@gmail.com>'

VERSTR      = MAJOR_VERSION + '.' + MINOR_VERSION
FULLVERSION = PROGRAM_NAME + ' ' + VERSTR + ', ' + COPYRIGHT



def main():
    args = parseargs()

    profname = args.profile if args.profile else 'default'
    profile = loadprofile(profname)
    datafile = os.path.expanduser('~') + '/.cache/' + PROGRAM_NAME + '/'
    try:
        datafile = datafile + profile['download'] + '.json'
    except KeyError:
        datafile = datafile + profname + '.json'

    if args.fetch:
        weather = fetch(profile)
        try:
            out = open(datafile, 'w')
            json.dump(weather, out, indent=4, separators=(',', ': '))
            out.close()
        except IOError:
            print "Cannot write cache file for '%s'." % profname
            exit(1)
    if not args.quiet:
        try:
            infile = open(datafile, 'r')
            data = json.load(infile)
            if args.output == None:
                print parseformat(profile['format'], data)
            else:
                print parseformat(args.output, data)
        except IOError:
            print "Cannot read cache file for '%s'." % profname
            exit(1)
        except KeyError:
            print "You must include a format string in your profile!"
            exit(1)

def parseformat(fmt, data):
    """Parse the given format string and return the formatted data.

    Arguments:
    fmt -- the format string to parse
    data -- the weather data to use
    """
    def lookup(data, keys):
        """Recursively look up an array of keys in nested dictionaries.

        Arguments:
        data -- nested dictionaries in which to look up the array of keys.
        keys -- array of keys to look up in the dictionary
        """
        if len(keys) == 1:
            return str(data[keys[0]])
        else:
            return lookup(data[keys[0]], keys[1:])

    def translate(match):
        """Translate a matched group into a data string using the given weather
        data. If the key does not exist, return the match group without the
        delimeters.

        Arguments:
        match -- the matched pattern to replace
        """
        try:
            keys = match.group().strip('%').split('/')
            return lookup(data, keys)
        except KeyError:
            return match.group().strip('%')

    # Cool regex to replace all '%thing%' with the value stored in
    # data['thing'], ignoring any escapes (eg '\%')
    out = re.sub(r"(?<!\\)%(.*?[^\\])%", translate, fmt)

    # Replace all the escapes with a regular symbol
    out = re.sub(r"\\%", "%", out)

    return out

def parseargs():
    """Parse the command line arguments and return the resulting NameSpace"""
    parser = argparse.ArgumentParser(description='Download and display ' \
                    'weather information from wunderground.', \
                    epilog=FULLVERSION)

    # Display version info
    parser.add_argument('-v', '--version',
            help='display version information and exit',
            action='version',
            version=FULLVERSION)

    # Command for downloading data from wunderground
    parser.add_argument('-f', '--fetch',
            help='download the latest weather data',
            action='store_true')

    # Specify the output format, rather than use the one in the profile
    parser.add_argument('-o', '--output',
            help='print the given output string',
            action='store')

    # Do not print the output
    parser.add_argument('-q', '--quiet',
            help='do not print weather data',
            action='store_true')

    # Specify the profile to use
    parser.add_argument('profile', nargs='?',
            help='select the profile to use',
            action='store')

    return parser.parse_args()


def loadprofile(profname):
    """Load the given profile from the filesystem and return the data.

    Arguments:
    profname -- the profile name to use
    """
    profpath = getprofpath(profname)

    # Try to open the profile
    try:
        f = open(profpath, "r")
        indata = f.read()
        # Stay away from my escapes, JSON!
        indata = re.sub(r"\\%", "\\\\\\\\%", indata)
        data = json.loads(indata)
        f.close()
    except IOError:
        print "Cannot open profile '%s'." % profname
        exit(1)
    except ValueError:
        print "Cannot parse profile '%s'." % profname
        exit(1)

    return data


def getprofpath(profname):
    """Get the path to the profile with the given name.

    Arguments:
    profname -- the profile name to use
    """
    global PROGRAM_NAME

    return os.path.expanduser('~') + '/.config/' + PROGRAM_NAME + '/' \
                                   + profname + '.json'

def fetch(profile):
    """Connect to the wunderground website using the given profile, and return
    the resulting JSON document.

    Arguments:
    profile -- the profile to use when connecting to wunderground
    """
    try:
        features = '/'.join(profile['features'])
    except KeyError:
        print 'You must specify features to use in your profile!'
        exit(1)

    try:
        query = profile['query']
    except KeyError:
        print 'You must specify a location to query in your profile!'
        exit(1)

    try:
        key = profile['devkey']
    except KeyError:
        print 'You must specify your dev key to download from wunderground!'
        exit(1)

    url = "http://api.wunderground.com/api/%s/%s/q/%s.json" \
            % (key, features, query)
    f = urllib2.urlopen(url)
    data = json.load(f)
    f.close()

    return data

if __name__ == "__main__":
    main()

