#/bin/bash
#Written by Vlatko Klabucar

if [ "$#" -ne 1 ]; then
    echo "USAGE: ./send-image.sh <SERVER-IP>"
    exit 0
fi

curl -X POST --data-binary @cute_otter.jpg http://$1:8880/upload-image
