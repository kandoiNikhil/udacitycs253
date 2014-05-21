import datetime
file = open('/home/kandoi/Desktop/Train/Train.csv','r')
count=0
time_start = datetime.datetime.now()
for line in file:
	count=count+1
time_end=datetime.datetime.now()
print count
print "Time Taken :" ,time_end-time_start
file.close()


