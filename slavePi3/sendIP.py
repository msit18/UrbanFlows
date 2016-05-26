import subprocess, os

ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
os.system('echo {0} | mail -s "Pi3 IP Address" msit@wellesley.edu'.format(ip_address))
