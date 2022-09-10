#!/bin/zsh

# Source: https://github.com/hkoba/zshscript-template/blob/master/bin/script.zsh

#----------------------------------------
# Reset options

emulate -L zsh

# set -eu

# setopt YOUR_FAVORITE_OPTIONS_HERE

setopt extended_glob

#----------------------------------------
# Set variables for application directory

# $0            = ~/bin/mytask
# $realScriptFn = /somewhere/myapp/bin/myscript.zsh
# binDir        = /somewhere/myapp/bin
# appDir        = /somewhere/myapp

realScriptFn=$(readlink -f $0); # macOS/BSD の人はここを変更
binDir=$realScriptFn:h
appDir=$binDir:h

#------
the_infocom_files_dir=$appDir/the_infocom_files
remoteUrl=$1

echo "Cloning $remoteUrl into $the_infocom_files_dir"

cd $the_infocom_files_dir
git submodule add $remoteUrl
