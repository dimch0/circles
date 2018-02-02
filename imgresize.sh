#!/bin/bash

if [ $# -ne 1 ]; then
    echo Please provide a directory name containing the images
    echo Example usage: imgresize.sh imagesdir
    exit 1
fi

IMGDIR="$1"
IMAGES="$(ls ${IMGDIR})"

for IMG in $IMAGES; do
    IMGPATH=${IMGDIR}/${IMG}
    echo "Resizing ${IMGPATH} ..."
    convert ${IMGPATH} -background none -gravity Center -extent 120x120 ${IMGPATH}

done
