#!/bin/bash

for directory in $@
do
  if [ -d $directory ]; then
    rm -r $directory
  fi
done

echo Cleaning done!