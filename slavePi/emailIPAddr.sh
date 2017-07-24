#!/bin/bash

#_IP=$(hostname -I)
echo "CRON pi address for 10.0.0.6 is $(hostname -I)" | mail -s "Pi6 address" urbanflowsproject@gmail.com




#IPAddr = Log IP address

#If the IP addr changes, send email
#if IPAddr != (call IP addr):
#	IPAddr = (call IP addr)

#If wifi is down. Send email when it gets back up IF IPaddr is different
