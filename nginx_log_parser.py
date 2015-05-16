__author__ = "Abhishek Singh Sambyal"
__email__ = "abhishek.sambyal@gmail.com"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3"

# Usuage: python nginx_log_parser.py

import re, time
from datetime import datetime

try:
	import httpagentparser
except ImportError:
	raise ImportError('httpagentparser module didn\'t load')


# Global Variable: store distinct HTTP statuses
LIST_SET = []


# Counting total enteries
# Parameter: log: example.log file
def count(log):
	number_of_entry = 0
	for line in log.xreadlines():
		number_of_entry = number_of_entry + 1
	print '--------------------Number of enteries: --------------------\n' + str(number_of_entry)


# Total no of failures
# Parameter: log: example.log file
def failure(log):
	fails = 0
	
	try:
		# Find all the occurrences of HTTP Status code
		match = re.findall(r'GET\s.+\s\w+/.+"\s([\d]+)\s', log.read())
	except:
		raise TypeError("The file HTTP status format is different.")
		
	# Number of failures
	for x in match:
		if x != '200': 
			fails = fails + 1
	print '\n--------------------Failures: --------------------\n' + str(fails)


# HTTP Status codes and their occurrences
# Parameter: log: example.log file
def http_status(log):
	
	try:
		# Find all the statuses in the log file
		status = re.findall(r'(GET\s.+\s\w+/.+"\s)([\d]+)\s', log.read())
	except:
		raise TypeError("The file GET and HTTP status format is different.")
		
	# Store distinct values of statuses
	global LIST_SET
	LIST_SET = list(set([x[1] for x in status]))
	
	# Print the status code and number of their occurrences
	print '\n--------------------HTTP Status codes and their occurrences--------------------'
	for a in xrange(len(LIST_SET)):
		print LIST_SET[a] + ': ' + str(([x[1] for x in status]).count(LIST_SET[a]))


# Find number of unique page visits on a URL
# Parameters: log: example.log file, N: time interval in seconds

# This subroutine creates a list of all the enteries of status code 200
# and takes each url with unique views.
# Diffent IP address, different time(difference more than N sec), different user agents is considered a unique visit. 
def pageviewparameters(log, N):
	global LIST_SET
	
	try:
		# Find all occurrences of IP address, HTTP Status code, URL, User agent
		total = re.findall(r'(\d+.\d+.\d+.\d+)\s-\s-\s\[(.+)\]\s\"GET\s.+\s\w+/.+\"\s(\d+)\s\d+\s\"(.+)\"\s\"(.+)\"',log.read())
	except:
		raise TypeError("The file format is different.")
		
	# Create all the valid visits which have 200 HTTP status
	# "view" variable will have all the enteries with HTTP status 200
	view = []
	[view.append(y) for y in total if y[2] == '200']
	enteries_in_view = len(view)
	
	# Collect all url's
	totalurl = []
	
	# Keep only unique url's
	uni_url = []
	
	# Collect all the urls
	for x in xrange(enteries_in_view):
		totalurl.append(view[x][3])
	
	# Keep unique urls
	uni_url = list(set(totalurl))
	
	# Collect all the enteries of each url
	count_list = []
	
	# Collect enteries of URL which have unique views
	unique_urls = []
	
	print '\n--------------------URL\'s and Unique Views--------------------\n'
	
	# Check for every unique URL
	for x in uni_url:
		count_list = []
		
		# Check entry with status 200
		for y in view:
			
			# Make a list of URL
			if y[3].rstrip() == x.rstrip():
				# IF true, store entry
				count_list.append(y)
		
		# Size of all entries of HTTP 200 with 'x' URL
		size_list = len(count_list)
		
		check = 0
		url_count = 0
		first_count = 0
		
		# Check size_list has more than 1 entry
		if size_list > 1:
			
			for k in count_list[1:]:
				
				# Store first entry as unique_url view list
				if first_count == 0:
					unique_urls.append(count_list[0])
					first_count = 1
				
				# Store next entry
				ipfield_next = k[0]
				
				# Check current entry and next entry IP addresses
				if unique_urls[url_count][0] == ipfield_next:
					
					# Current entry user agent
					user_agent1 = httpagentparser.simple_detect(unique_urls[url_count][4])
					
					# Next entry user agent
					user_agent2 = httpagentparser.simple_detect(k[4])
					
					# Check current and next user agent values
					if user_agent1[0] == user_agent2[0] and user_agent1[1] == user_agent2[1]:
						
						try:
							# Find the time between the two requests
							first_time = re.search(r'(\d+/\w+/\d+:\d+:\d+:\d+)\s', unique_urls[url_count][1])
							second_time = re.search(r'(\d+/\w+/\d+:\d+:\d+:\d+)\s', k[1])
						except:
							raise TypeError("The file day and date format is different.")	
							
						FMT = '%d/%b/%Y:%H:%M:%S'
						tdelta = datetime.strptime(second_time.group(1), FMT) - datetime.strptime(first_time.group(1), FMT)
						total_sec = tdelta.total_seconds()
						
						# If time between two requests are greater than the input time, consider it a unique visit
						if total_sec > N:
							
							# Store it as a unique view
							unique_urls.append(k)
							url_count = url_count + 1
						
						# If time is lesser than the given input discard that view and continue
						else:
							continue
					
					# If user agents are different
					# Store it as a unique view
					else:
						unique_urls.append(k)
						url_count = url_count + 1
						
				# If IP addresses are different
				# Store it as a unique view
				else:
					unique_urls.append(k)
					url_count = url_count + 1
			
			# Display URL's and their unique visits
			print unique_urls[0][3], ' :', str(len(unique_urls))
			
			unique_urls = []
			count_list = []
			
		# Only 1 URL with HTTP 200 Status
		# Cosider is a unique visit
		else:
			print count_list[0][3], " : ", str(1)	


def main():
	start_time = time.time()
	
	# Reading log file 
	try:
		logfile = open('example.log', 'r')
	except IOError:
		raise IOError('The input file does not exist, please check the path.')
		
	# Counting total log enteries
	count(logfile)
	logfile.seek(0)
	
	# Processing faliures
	failure(logfile)
	logfile.seek(0)
	
	# Number of log enteries by HTTP status code
	http_status(logfile)
	logfile.seek(0)
	
	#URL and Unique visits
	pageviewparameters(logfile, 1)
	
	logfile.close()
	print "--- %s seconds ---" % (time.time() - start_time)
	

if __name__ == '__main__':
	main()
