#!/usr/bin/env python3

import sys
import argparse
import requests
from lxml import html
import urllib3

# Nobody wants to see SSL warnings :-P
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def doSleep(timing):

	if timing == 0:
		time.sleep(random.randrange(90,120))
	elif timing == 1:
		time.sleep(random.randrange(60,90))
	elif timing == 2:
		time.sleep(random.randrange(30,60))
	elif timing == 3:
		time.sleep(random.randrange(10,20))
	elif timing == 4:
		time.sleep(random.randrange(5,10))

def getHostnames(domain):

	url = 'https://crt.sh/?q={0}'.format(domain)
	headers = {'User-Agent': useragent,
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Language': 'en-US,en;q=0.5',
		   'Accept-Encoding': 'gzip, deflate',
		   'Referer': 'https://crt.sh/'}

	try:

		r = requests.get(url,headers=headers,proxies=proxies,verify=False)
		if r.status_code == requests.codes.ok:
			tree = html.fromstring(r.text)
			crtsh_hostnames = [x.lower() for x in tree.xpath('//td[@class="outer"]/table/tr/td[5]/text()')]

			# Clean up the list for valid hostnames
			hostnames = []
			for hostname in crtsh_hostnames:
				if hostname not in hostnames and '*' not in hostname:
					hostnames.append(hostname)

			# Print hostnames
			for hostname in hostnames:
				print(hostname)

	except Exception as e:
		print('[!] An exception occurred while querying crt.sh: {0}'.format(e))

if __name__ == "__main__":

	parser = argparse.ArgumentParser(
	description='Extracts hosts from certificate transparency logs at cert.sh',
	epilog = '''
Examples:
./{0} -d google.com
./{0} -f domains.txt'''.format(sys.argv[0]),
	formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('-d','--domain', help='Domain to query certificate transparency logs for', required=False, default=None, type=str, dest='domain')
	parser.add_argument('-f','--file', help='File containing domains to query certificate transparency logs for', required=False, default=None, type=str, dest='file')
	parser.add_argument('-t','--timing', help='Modifies request timing to avoid getting banned for being a bot. Slowest(0) = 90-120 seconds, Default(3) = 10-20 seconds, Fastest(5) = no delay', required=False, default=3, type=int, choices=range(0,6), dest='timing')
	parser.add_argument('-p', '--proxy', help='Proxy example: http://127.0.0.1:8080', required=False, default=None, type=str, dest='proxy')
	parser.add_argument('-u', '--useragent', help='User agent string to make requests with', required=False, default='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', type=str, dest='useragent')

	args = parser.parse_args()

	# Global Variables

	useragent = args.useragent
	if args.proxy:
		proxies = {'http': args.proxy, 'https': args.proxy}
	else:
		proxies = None
	
	if args.file:
		try:
			with open(args.file) as f:
				domains = [line.rstrip('\n') for line in f]
		except Exception as e:
			print('[!] Trouble opening file {0}\n\n{1}\n\n'.format(args.file,e))
			exit(1)
	elif args.domain:
		domains = [args.domain]
	else:
		print('[!] Either a domain (-d, --domain) or file containing domains (-f, --file) is required!')
		exit(1)

	# Main logic

	for domain in domains:
		getHostnames(domain)
