__author__ = "Abhishek Singh Sambyal"
__email__ = "abhishek.sambyal@gmail.com"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3"

import re, httpagentparser
from datetime import datetime

LIST_SET = []

#Counting total enteries
def count(log):
	number_of_entry = 0
	for line in log.xreadlines():
		number_of_entry = number_of_entry + 1
	print 'Number of enteries: ' + str(number_of_entry)


#Total no of failures
def failure(log):
	fails = 0
	match = re.findall(r'(GET\s.+\s\w+/.+"\s)([\d]+)\s', log.read())
		
	#Number of failures
	for x in match:
		if x[1] != '200': 
			fails = fails + 1
	print '\nFailures: ' + str(fails)


#HTTP Status codes and their occurrences
def http_status(log):
	status = re.findall(r'(GET\s.+\s\w+/.+"\s)([\d]+)\s', log.read())
	
	#converting set to list 
	global LIST_SET
	LIST_SET = list(set([x[1] for x in status]))
	
	#printing the status code and the number of their occurrences
	print '\nHTTP Status codes and their occurrences'
	for a in xrange(len(LIST_SET)):
		print LIST_SET[a] + ': ' + str(([x[1] for x in status]).count(LIST_SET[a]))


	
def pageviewparameters(log, N):
	global LIST_SET
	total = re.findall(r'(\d+.\d+.\d+.\d+)\s-\s-\s\[(.+)\]\s\"GET\s.+\s\w+/.+\"\s(\d+)\s\d+\s\"(.+)\"\s\"(.+)\"',log.read())
	a = set(total)
	test_var = total[0:2005]
	
	# Creating all the valid visits which have 200 HTTP status
	view = []
	if '200' in LIST_SET:
		[view.append(y) for y in test_var if y[2] == '200']
		
	totalurl = []
	uni_url = []
	enteries_in_view = len(view)
	
	#Collecting all the urls in log file
	for x in xrange(enteries_in_view):
		totalurl.append(view[x][3])
	#print '0000000000000000000000000'
	#print totalurl
	
	# Unique url in total url using set
	uni_url = list(set(totalurl))
	
	#print view[0][4]
	user_ag = httpagentparser.simple_detect(view[0][4])
	#print user_ag[1]
		
	count_list = []
	#print 'hhhhhhhhhi'
	#print view[0][3]
	unique_urls = []      
	time_filter = []
	#print uni_url
	#print 'hiiiiii'
	
	for x in uni_url:
		count_list = []
		for y in view:
			if x.rstrip() == y[3].rstrip():
				count_list.append(y)
		size_list = len(count_list)
		#pprint count_list[0]
		#print count_list[1]
		
		#print '-----count_list-------'
		#print count_list
		boundvar = 1
		check = 0
		url_count = 0
		#for x in xrange(len(count_list)):
		#	time_filter.append(re.findall(r'\d+/\w+/\d+:(\d+:\d+:\d+)\s', count_list[x][1]))
		for k in count_list:
			if boundvar < size_list:
				print boundvar
				print '-------------------k---------------'
				print k
				print '-------------------input field _ next---------------'
				ipfield_next = count_list[boundvar][0]
				print ipfield_next
				#print '4444444'
				#ipfield_next = count_list[boundvar+1][0]
				#print '5555555555'
				#print boundvar, size_list
				#print ipfield, ipfield_next
				print"-----------count_list------------"
				print count_list
				#Checking if IP address of two consecutive positions
				if url_count == 0:
					unique_urls.append(k)
				print '------------unique_urls----------------'
				print unique_urls[url_count][0]
				print unique_urls
				if unique_urls[url_count][0] == ipfield_next:
					#print '---------------------------------YYYYYYYYYYYYYYYYYSSSSSSSSSSSSSSSSS ipfield'
					#User Agent
					user_agent1 = httpagentparser.simple_detect(unique_urls[url_count][4])
					user_agent2 = httpagentparser.simple_detect(count_list[boundvar][4])
					if user_agent1[0] == user_agent2[0] and user_agent1[1] == user_agent2[1]:
						print '---------------------------------YYYYYYYYYYYYYYYYYSSSSSSSSSSSSSSSSS user_agent'
						#print '------------'
						#print user_agent1[0]
						#print user_agent1[1]
						#print '------------'
						#print user_agent2[0]
						#print user_agent2[1]
						print"----------user_agent1-------------"
						print user_agent1
						print"---------user_agent2------------"
						print user_agent2
						# Find the time between the two requests
						first_time = re.search(r'\d+/\w+/\d+:(\d+:\d+:\d+)\s', unique_urls[url_count][1])
						print '---------first_time---------'
						print first_time.group(1)
						second_time = re.search(r'\d+/\w+/\d+:(\d+:\d+:\d+)\s', count_list[boundvar][1])
						print '---------second_time---------'
						print second_time.group(1)						
						FMT = '%H:%M:%S'
						tdelta = datetime.strptime(second_time.group(1), FMT) - datetime.strptime(first_time.group(1), FMT)
						diff_in_time = getSec(str(tdelta))
						print '-----------------time difference------------'
						print diff_in_time
						# If time between two requests are greater than the input time, consider it a unique visit
						if diff_in_time > N:
							print '---------------------------------YYYYYYYYYYYYYYYYYSSSSSSSSSSSSSSSSS difference'
							print '------------unique_urls----------------'
							unique_urls.append(count_list[boundvar])
							print unique_urls
							print '------------url_count----------------'
							url_count = url_count + 1
							print url_count
							print '------------boundvar----------------'
							boundvar = boundvar + 1
							print unique_urls
							#if boundvar == size_list - 1:
						#		check = 1
						#		print 'yesssssss'
			#			#	print 'nooooooo'
						else:
							boundvar = boundvar + 1
				else:
					unique_urls.append(count_list[boundvar])
					url_count = url_count + 1
					boundvar = boundvar + 1
					#if boundvar == size_list - 1:
						#check = 1
			#		print 'yesssssss'
					
			#boundvar = boundvar + 1
			#print '-----------unique_urls-----------'
			#print unique_urls
			#if check == 1:
				#print 'cheeeeeeeeeeeeekkkkkkk'
			#	unique_urls.append(k)
			#	check = 0
			#else:
			#	continue
			#url_count = url_count + 1
		print"---------unique_urls--------------"
		print unique_urls
		break
	#print'2222222222222'
	##print count_list[0]
	#print count_list[0][1]
	#print count_list[len(count_list)-2:len(count_list)]
	#print count_list
	#return
		print '-------------------'
	#print time_filter			
	#s1 = time_filter[0][0]
	#print s1
	#s2 = time_filter[1][0]
	#print s2
	#FMT = '%H:%M:%S'
	#tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
	#print getSec(str(tdelta))

# Calculate the seconds
def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
	
def main():
	
	## reading log file 
	logfile = open('example.log', 'r')
	
	#Counting total log enteries
	count(logfile)
	logfile.seek(0)
	
	#Processing faliures
	failure(logfile)
	logfile.seek(0)
	
	#Number of log enteries by HTTP status code
	http_status(logfile)
	logfile.seek(0)
	
	pageviewparameters(logfile, 1)
	
	logfile.close()

if __name__ == '__main__':
	main()