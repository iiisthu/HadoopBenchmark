import subprocess
import sys
import re
import pdb
#import numpy
import datetime
import time
#import os
if len(sys.argv) < 4:
	print len(sys.argv)
	print 'usage: python collect_data.py [hostip] [check interval] [start date:hour:minute]  '
	sys.exit()

host=sys.argv[1]
ty=sys.argv[3]
[date,hour,minute] = ty.split(':')
interval=int(sys.argv[2])
#host='10.1.0.50'
IFSTATS="ifstat  -i eth5 -i vp0 -i eth0 1 2"
IOSTATS="iostat -y -m 1 1"
CPU_MEM="mpstat 1 2 | grep Average && free -m  | grep 'buffers/cache'"
class prettyfloat(float):
	def __repr__(self):
		return "%0.2f" % self
def network(output,stats):
	res1 = output[2].strip().split()
	res2 = output[3].strip().split()
	ave = [ "%.1f"%(sum(x)/2) for x in zip(map(prettyfloat, res1),map(prettyfloat,res2)) ]
	stats['ETH5_IN'] = ave[0]
	stats['ETH5_OUT'] = ave[1]
	stats['VP0_IN'] = ave[2]
	stats['VP0_OUT'] = ave[3]
	stats['ETH0_IN'] = ave[4]
	stats['ETH0_OUT'] = ave[5]

def io(output,stats):
	for i,line in enumerate(output):
		data={}
		list_tmp = line.strip().split()
#		data['READ_OPER']=list_tmp[3]
#		data['WRITE_OPER']=list_tmp[4]
#		data['READ_SEC']=list_tmp[5]
#		data['WRITE_SEC']=list_tmp[6]
#		data['AVGRQ_SZ']=list_tmp[7]
#		data['AVGQU_SZ']=list_tmp[8]
#		data['AWAIT']=list_tmp[9]
#		data['SVCTM']=list_tmp[10]
#		data['UTIL']=list_tmp[11]
		data['MBREAD']=list_tmp[2]
		data['MBWRITE']=list_tmp[3]
		index=str(i)
		stats['DISK'+index]=data

def cpu_mem(output,stats):
	cpu = output[0]
	mem = output[1]
	cpudata = {}
	memdata = {}
	list_tmp=mem.strip().split()
	memdata['USED']=list_tmp[2] 
	list_tmp=cpu.strip().split()
	cpudata['USR'] = list_tmp[2]
	cpudata['SYS'] = list_tmp[4]
	cpudata['IOWAIT'] = list_tmp[5]
	cpudata['IDLE'] = list_tmp[10]
	stats['CPU'] = cpudata
	stats['MEM'] = memdata

def ssh_client(host,command,service):
	ssh = subprocess.Popen( ["/bin/sh","-c" ,command],
			shell=False,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	if result == []:	
		error = ssh.stderr.readlines()
		print >>sys.stderr, "ERROR: %s" % error
	else:
		if service == 'Network':
			arr={}
			network(result,arr)
			return arr
		if service == 'DiskIO':
			arr={}
			io(result,arr)
			return arr
		if service == 'CPUMEM':
			arr={}
			cpu_mem(result,arr)
			return arr
def addSecs(tm, secs):
	fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
	fulldate = fulldate + datetime.timedelta(seconds=secs)
	return fulldate
def totalseconds(td):
	return 1+(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
def LOG(log,str):
    log.write('%s'%(datetime.datetime.now())+str+'\n' )

id=(host.split('.'))[3]
print "Create files..."
log= open('/home/shenh10/system_monitor/results/sys_log'+id, 'a')

ts=datetime.datetime(2015,6,int(date),int(hour),int(minute),0,0)
now =  datetime.datetime.now()
LOG(log,"expected time: %s,actual time: %s"%(ts,now))
if now > ts:
	LOG(log,"Start time in the past! exit... ")
	sys.exit(1)

while now < ts:
	td=totalseconds(ts-now)
	LOG(log,"Waiting for %s s...."%td)
	time.sleep(td)
	now =  datetime.datetime.now()
	continue

print "Start task..."
LOG(log, "task begin at %s"%now)
outfile= open('/home/shenh10/system_monitor/results/sys_stats'+id, 'a')
count=0
while 1 : 
	print "start round %s monitor"%count
	stats_all={}
	data={}
	LOG(log,"start test")
	data['Network']=ssh_client(host,IFSTATS,'Network')
	if int(id) > 75:
		data['DiskIO']=ssh_client(host, IOSTATS+' | grep sd[g-i]','DiskIO')
	else:
		data['DiskIO']=ssh_client(host, IOSTATS+' | grep sd[b-d]','DiskIO')
	data['CPUMEM']=ssh_client(host, CPU_MEM,'CPUMEM')
	print "finish round %s monitor"%count
	count=count+1
	stats_all['TIMESTAMP']="%s"%ts
	stats_all['HOST']=host
	stats_all['SYSINFO']=data
	ts = addSecs(ts,interval)
	outfile.write('%s\n'%stats_all)
        outfile.flush()
	LOG(log,"finish test")
	while ts < datetime.datetime.now():
		LOG(log,"Time unmatched! Adjusting!...")
		ts = addSecs(ts,interval)
	now = datetime.datetime.now()
	totalsec = totalseconds(ts-now)
	LOG(log,"sleep %s  s..."%totalsec)
        log.flush()
	time.sleep(totalsec)
LOG(log,"Done,close files")
outfile.close()
log.close()
