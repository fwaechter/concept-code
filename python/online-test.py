#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import socket
import argparse

def socket_check(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	try:
		s.connect((host, int(port)))
		print "Host: " + host + " Port: " + str(port) + " open"
	except Exception, e:
		print "Host: " + host + " Port: " + str(port) + " " + str(e)
	s.close()

def initialize_check(host, minport, maxport, timeout):
	if int(minport) > int(maxport):
		print "minport > maxport"
	while int(minport) <= int(maxport):
			socket_check(host, int(minport))
			minport = int(minport) + 1

def parse_options():
	parser = argparse.ArgumentParser()
	parser.add_argument('host', help='host ip')
	parser.add_argument('minport', help='port to start with')
	parser.add_argument('maxport', help='last port to check')
	parser.add_argument('timeout', help='set timeout')
	return parser

def main (argv=None):
	if argv is None:
		argv = sys.argv[1:]
	option_parser = parse_options()
	args = option_parser.parse_args(argv)
	initialize_check(args.host, args.minport, args.maxport, args.timeout)

if __name__ == '__main__':
	main()

