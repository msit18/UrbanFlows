sshpass -p 'ravenclaw' scp Pi9_RW1600_RH1200_TT300_FR15_01_31_2017_16_22_00_207871.h264 msit@18.89.4.173:/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/

rsync -vh --dry-run Pi9_RW1600_RH1200_TT300_FR15_01_31_2017_16_22_00_207871.h264 msit@18.89.4.173:/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/


/usr/bin/rsync -vh --rsh="/usr/bin/sshpass -p ravenclaw ssh -o StrictHostKeyChecking=no -l msit" Pi9_RW1600_RH1200_TT300_FR15_01_31_2017_16_22_00_207871.h264 msit@18.89.4.173:/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/
rsync --remove-source-files --timeout=300 -vhe "sshpass -p ravenclaw ssh" Pi9_RW1600_RH1200_TT300_FR15_01_31_2017_16_22_00_207871.h264 msit@18.89.4.173:/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/

if [ "$?" -eq "0" ];
then
	echo $?
    echo "SUCCESS"
else
	echo $?
    echo "FAIL $?"
fi