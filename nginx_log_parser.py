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


	
def pageviewparameters(log):
	global LIST_SET
	total = re.findall(r'(\d+.\d+.\d+.\d+)\s-\s-\s\[(.+)\]\s\"GET\s.+\s\w+/.+\"\s(\d+)\s\d+\s\"(.+)\"\s\"(.+)\"',log.read())
	#print time_filter.group(1)
	#print len(total)
	a = set(total)
	#print len(a)
	#print total[0:3]
	test_var = total[0:2005]
	#print test_var[2][2]
	#print LIST_SET
	#print LIST_SET[2]
	view = []
	if '200' in LIST_SET:
		[view.append(y) for y in test_var if y[2] == '200']
	#print view[0:10]
	#print len(view)
	#print view[0][3]
	#print view[1][1]
	#print view[2][1]
	time_filter = []
	totalurl = []
	uni_url = []
	enteries_in_view = len(view)
	#print enteries_in_view
	for x in xrange(enteries_in_view):
		time_filter.append(re.findall(r'\d+/\w+/\d+:(\d+:\d+:\d+)\s', view[x][1]))
		totalurl.append(view[x][3])
	#print view[0][3]
	#print time_filter[0]
	#print time_filter[1]
	#print time_filter[2]
	#print totalurl
	uni_url = list(set(totalurl))
	
	#print view[0][4]
	user_ag = httpagentparser.simple_detect(view[0][4])
	#print user_ag[1]
	
	z=0
	
	count_list = []
	#print 'hhhhhhhhhi'
	#print view[0][3]
	unique_urls = []
	#print uni_url
	#print 'hiiiiii'
	
	for x in uni_url:
		for y in view:
			if x.rstrip() == y[3].rstrip():
				count_list.append(y)
		size_list = len(count_list)-1
		#pprint count_list[0]
		#print count_list[1]
		
		print '------------'
		print count_list
		boundvar = 0
		check = 0
		for k in count_list:
			if boundvar < size_list:
				print boundvar
				ipfield = count_list[boundvar][0]
				#print '4444444'
				#print count_list[1][0]
				ipfield_next = count_list[boundvar+1][0]
				#print '5555555555'
				#print count_list[2][0]
				print '1111111'
				print boundvar, size_list
				print ipfield, ipfield_next
				if ipfield != ipfield_next:
					unique_urls.append(k)
					if boundvar == size_list - 1:
						check = 1
					print 'yesssssss'
				else:
					print 'nooooooo'
			boundvar = boundvar + 1
		if check == 1:
			print 'cheeeeeeeeeeeeekkkkkkk'
			unique_urls.append(k)
			check = 0
		else:
			continue
		
		print '3333333333'
		print unique_urls
		return
	#print'2222222222222'
	##print count_list[0]
	#print count_list[0][1]
	#print count_list[len(count_list)-2:len(count_list)]
	#print count_list
	#return
	
				
	s1 = time_filter[0][0]
	#print s1
	s2 = time_filter[2][0]
	#print s2
	FMT = '%H:%M:%S'
	tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
	#print tdelta
	
	
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
	
	pageviewparameters(logfile)
	
	logfile.close()

if __name__ == '__main__':
	main()
	
    