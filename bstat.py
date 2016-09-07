#! /usr/bin/env python

import re

def main():
	try:
		state = open('/proc/acpi/battery/BAT0/state', 'r').read()
		info = open('/proc/acpi/battery/BAT0/info', 'r').read()
	except IOError:
		print 'Can\'t find your battery information files'
		exit()
	cap = int(re.search(r'design capacity.*?(\d+) mAh', info).group(1))
	curcap = int(re.search(r'last full capacity.*?(\d+) mAh', info).group(1))
	amtleft = int(re.search(r'remaining capacity.*?(\d+) mAh', state).group(1))
	rate = int(re.search(r'present rate:.*?(\d+) mA', state).group(1))
	cstate = re.search(r'charging state:\s+?(\w+)', state).group(1)
	if cstate == 'charging':
		tocharge = curcap - amtleft
		tleft = float(tocharge)/rate
		p = float(curcap)/cap * 100
		print 'Health: %.0f percent: %d/%d mAh\nCharging: %.0f percent: %d mAh left to charge at a rate of %d mA\n%.2f hours until fully charged' % (p, curcap, cap, 100*float(amtleft)/curcap, tocharge, rate, tleft)
	elif cstate == 'discharging':	 
		tleft = float(amtleft)/rate
		p = float(curcap)/cap * 100
		print 'Health: %.0f percent: %d/%d mAh\nDischarging: %.0f percent: %d mAh left being used at a rate of %d mA\n%.2f hours left' % (p, curcap, cap, 100*float(amtleft)/curcap, amtleft, rate,tleft)
	elif cstate == 'charged':
		p = float(curcap)/cap * 100
		print 'Health: %.0f percent: %d/%d mAh\nFully Charged' % (p, curcap, cap)

if __name__ == '__main__':
	main()
