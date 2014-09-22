#!/bin/sh

VERSION="0.1"

# Print usage statement and exit
usage()
{
    echo "usage: $0 [-h] [-v] [-f] <profile> [target]"
    exit
}

# Print version information and exit
version()
{
    echo "wprofile $VERSION, Copyright (c) 2014 Brian Kubisiak " \
        "<velentr.rc@gmail.com>"
    exit
}

# do not remove default.json
force=0

while getopts ":hvf" opt; do
    case $opt in
        h)
            usage
            ;;
        v)
            version
            ;;
        f)
            # remove default.json if it exists
            force=1
            ;;
        \?)
            echo "Unknown option: -$OPTARG"
            ;;
    esac
done

# profile and target must be last two arguments
profile=${@:$OPTIND:1}
target=${@:$OPTIND+1:1}

# default target is default.json
if [ ! $target ]; then
    target="default"
fi

cd ~/.config/winfo

if [ -e "./${profile}.json" ]; then
    if [ ! -e "./${target}.json" ] || [ -h "./${target}.json" ] || [ $force -eq 1 ]; then
        rm -f "./${target}.json"
        ln -s "./${profile}.json" "./${target}.json"
    else
        echo "${target}.json exists! Rerun with '-f' to overwrite."
    fi
else
    echo "${profile}.json does not exist!"
fi

