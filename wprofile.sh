#!/bin/sh

VERSION="0.2"

# Print usage statement and exit
usage()
{
    echo "usage: $0 [-h] [-v] [-f] [-e] <profile> [target]"
    exit
}

# Print version information and exit
version()
{
    echo "wprofile $VERSION, Copyright (c) 2014 Brian Kubisiak " \
        "<velentr.rc@gmail.com>"
    exit
}

# do not remove default.json by default
force=0

# do not edit profile by default
edit=0

for opt in $@; do
    case $opt in
        -h)
            usage
            ;;
        -v)
            version
            ;;
        -f)
            force=1
            ;;
        -e)
            edit=1
            ;;
        *)
            if [ ! $profile ]; then
                profile=$opt
            elif [ ! $target ]; then
                target=$opt
            else
                usage
            fi
            ;;
    esac
done

# default target is default.json
if [ ! $profile ]; then
    usage
elif [ ! $target ]; then
    target="default"
fi

cd ~/.config/winfo

if [ -e "./${profile}.json" ]; then
    if [ $edit -eq 1 ]; then
        if [ ! $EDITOR ]; then
            echo "\$EDITOR is not defined!"
            exit
        else
            $EDITOR "./${profile}.json"
        fi
    elif [ ! -e "./${target}.json" ] || [ -h "./${target}.json" ] || [ $force -eq 1 ]; then
        rm -f "./${target}.json"
        ln -s "./${profile}.json" "./${target}.json"
    else
        echo "${target}.json exists! Rerun with '-f' to overwrite."
    fi
else
    echo "${profile}.json does not exist!"
fi

