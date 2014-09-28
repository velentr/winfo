# winfo

A simple command-line utility to display weather information from wunderground.

# Installation

The script uses Python 2; no other external libraries are needed. Simply copy
the script somewhere in your path, then `chmod +x`. You must also set up your
profile for the script to use (see the configuration section below for details).

# Usage

`winfo` aims to be incredibly simple to use: after your profile is set up,
running `winfo -f <profile>` will fetch new weather data before printing it, and
`winfo <profile>` will display the data. To fetch data without printing it, run
`winfo -f -q`. If no profile is specified, then 'default' is used. To specify
the output format on the command line, use the `-o <output>` argument. This will
override the format in the loaded profile.

Two other command-line options, `-h` and `-v`, are available for showing help
and version information (respectively).

## wprofile

This script is provided to help managing profiles. If, for example, you often
travel between Chicago and New York City, and have profiles `chicago.json` and
`nyc.json` for these, `wprofile` can help to switch between these locations.
Running `wprofile chicago` will symlink `chicago.json` to `default.json`,
displaying the chicago data by default. `wprofile` also accepts an optional
target name to use instead of 'default'.

This script can also be used to open the specified profile in your default
editor (uses the `$EDITOR` environment variable). To do this, use the `-e`
option: `wprofile -e <profname>`.

# Configuration

Configuration for `winfo` is done via JSON profiles stored in
`~/.config/winfo/*.profile`. Each profile must contain a features array, a query
location, a devkey developer's key from
[wunderground](http://www.wunderground.com/weather/api), and a format to print
the output as. The features and query that are available, along with variables
to print in the format string, are specified in the [API
documentation](http://www.wunderground.com/weather/api/d/docs?d=data/index).
Optionally, the profile may contain a download string, to allow multiple
profiles to read the same downloaded data.

To see examples, read the `default.json` included in this repo.

## features

This must be a JSON array listing all the features that you want to download
from wunderground (e.g. "conditions", "geolookup", etc.).

## query

This specifies the location to use for weather information. There are a variety
of options here, including postal code or state/city. Look at wunderground's
documentation for all the possibilities.

## devkey

In order to use this, you must get a developer's key from wunderground. It's
pretty easy to do, and free for low-volume usage.

## format

The format string is what `winfo` will print when it is run. It can contain
plain text and any escape characters supported by JSON. In addition, any strings
enclosed in percent signs (%) will be substituted with the wunderground data
corresponding to that string, where forward slashes (/) denote nested levels in
the data. In order to index into JSON arrays, all numerical values will be
parsed into integers as used as indices instead of keys. Note that array
indexing still uses forward slashes as delimeters.

For example, the string `%current_observation/weather%,
%current_observation/temp_f% F` might be printed out as `Scattered Clouds, 71.0
F`.

In order to use a literal percent, escape it with a backslash (e.g. '\%').

## download

By default, the profile `~/.config/winfo/prof.json` will download and read data
from `~/.cache/winfo/prof.json`. However, if the download string is set in the
profile (e.g. `"download": "output"`), then `winfo` will download and read data
from `~/.cache/winfo/output.json`. This allows multiple profiles to share the
same downloaded data.

# Copyright

Copyright (c) 2014 Brian Kubisiak <velentr.rc@gmail.com>

Comments, complaints, suggestions, etc. are all welcome.

# TODO

- [x] extend format strings to allow arbitrary categories
- [x] write scripts for managing profiles
- [x] document wprofile script
- [x] allow array indexing in output format
- [x] add `-o` argument to specify output format
- [x] fix `-o` argument to allow escape sequences
- [x] fix getopt in wprofile to allow args in any order
- [ ] better documentation

