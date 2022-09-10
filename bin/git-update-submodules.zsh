#!/bin/zsh

#----------------------------------------
# Reset options

emulate -L zsh

# set -eu

# setopt YOUR_FAVORITE_OPTIONS_HERE

setopt extended_glob

git submodule update --init --recursive