if balExp=$(curl -X GET http://18.189.122.45:8880/upload-image);
then curl --header "filename: img.jpg" -y 10 --max-time 180 -X POST --data-binary @img.jpg http://18.189.122.45:8880/upload-image &
wait;
rm img.jpg;
else sudo ifup wlan0;
fi