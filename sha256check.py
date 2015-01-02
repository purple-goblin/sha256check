#!/usr/bin/python

# This script checks to see whether the OpenBSD mirrors all report the same
# sha256 for the install56.iso file. Checks both 32-bit and 64-bit versions.

from bs4 import BeautifulSoup
import urllib2

url32 = '5.6/i386/SHA256'
url64 = '5.6/amd64/SHA256'
sha256_32 = 'd5763699a35e4b868039b2a0f3abcb12e119588677e51cedbf011c16e5ca8dc7'
sha256_64 = 'b38e1314b487d0970549fab1ae3ad7617d0d29a7bae52ea968d1d1d85d6bf433'
headers = {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)'}

# functions
def getsha256(url,real_sum):
	req = urllib2.Request(url,None,headers)
	try:
		reply = urllib2.urlopen(req).readlines()
		for i,s in enumerate(reply):
			if 'SHA256 (install56.iso)' in s:
				sha256 = reply[i].strip().split('= ')[1]
				if sha256 != real_sum:
					print "ERROR: %s != %s (%s)" % (sha256,real_sum,url)
				elif sha256 == real_sum:
					if 'i386' in url:
						print '  Match for 32-bit in %s' % url
					if 'amd64' in url:
						print '  Match for 64-bit in %s' % url
	except:
		print '\nERROR: %s\n' % url

def cycleLinks(links,sha256_32,sha256_64):
	for link in links:
		print 'Searching %s' % str(link['href'])
		base  = link['href']
		# these two mirrors are defective
		if 'mirrors.isu.net.sa/pub/ftp.openbsd.org' in base:
			break
		if 'http://www.obsd.si/pub/OpenBSD' in base:
			break
		# check 32-bit sha256
		url   = base + url32
		getsha256(url,sha256_32)
		# check for 64-bit sha256
		url   = base + url64
		getsha256(url,sha256_64)

# get the openBSD page which points to all their mirrors
main   = urllib2.urlopen('http://www.openbsd.org/ftp.html').read()
soup   = BeautifulSoup(main)
tables = soup("table")

print '\nNow checking the HTTP mirrors...\n'
table = tables[0]
links = table("a")
cycleLinks(links,sha256_32,sha256_64)

print '\nNow checking the FTP mirrors...\n'
table = tables[1]
links = table("a")
cycleLinks(links,sha256_32,sha256_64)

print 'Done!'
