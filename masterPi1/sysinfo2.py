#!/usr/bin/env python3
import sys
import subprocess
from time import sleep
import pifacecad


UPDATE_INTERVAL = 10 #60 * 5  # 5 mins
GET_IP_CMD = "hostname --all-ip-addresses"

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_my_ip():
    return run_cmd(GET_IP_CMD)[9:-1]

def get_my_ETH0IP():
    return run_cmd(GET_IP_CMD)[:9]

def wait_for_ip():
    ip = ""
    if len(ip) <= 0:
        sleep(1)
	ip = get_my_ip()

def show_sysinfo():
    while True:
        cad.lcd.clear()
        cad.lcd.write("IP:{}\n".format(get_my_ip()))

	cad.lcd.write("IP:{}".format(get_my_ETH0IP()))
        sleep(UPDATE_INTERVAL)
	cad.lcd.clear()
	sys.exit()

if __name__ == "__main__":
    cad = pifacecad.PiFaceCAD()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()

    if "clear" in sys.argv:
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.backlight_on()
        cad.lcd.write("Waiting for IP..")
        wait_for_ip()
        show_sysinfo()
