#import matplotlib.pyplot as plt
import os
import sys
import yaml
import datetime
import subprocess
import functools
import operator
import pdb
import collections
#Mem Usage


sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/%s'%sys.argv[3]
outpath='%s/out'%sourceFolder
if not os.path.exists(outpath):
    os.makedirs(outpath)
cpu_out = '%s/cpu'%(outpath)
mem_out = '%s/mem'%(outpath)
disk_out = '%s/disk'%outpath
net_out= '%s/net'%outpath
starttime=sys.argv[1]
endtime=sys.argv[2]
option=sys.argv[3]

# [s_date,s_hour,s_minute,s_second] = starttime.split(':')
# [e_date,e_hour,e_minute,e_second] = endtime.split(':')

interval = 5


def convertDate(str):
	return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

def totalseconds(td):
        return 1+(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


def count_lines(stime,etime):
	if etime < stime:
		return -1
	est_lines=totalseconds(etime-stime)/interval
	return est_lines

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def addSecs(tm, secs):
        fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + datetime.timedelta(seconds=secs)
        return fulldate

def yieldTime(starttime,endtime):
	t = starttime
	while t<= endtime:
		yield t
		t = addSecs(t,interval)

class prettyfloat(float):
        def __repr__(self):
                return "%0.2f" % self

def CPU_analysis(allCont):
	usage={'USR':[],'SYS':[],'IOWAIT':[],'IDLE':[]}
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	print nodeNum
	print timeLen
	for index in xrange(timeLen):
		cpu_all= [ allCont[i][index]['SYSINFO']['CPUMEM']['CPU'] for i in xrange(nodeNum)]
		tmp = [0,0,0,0]
		for value in cpu_all:
			for i,key in enumerate(usage.keys()):
				tmp[i] += prettyfloat(value[key])
		for i,key in enumerate(usage.keys()):
			usage[key].append(tmp[i]/nodeNum/100)
	with open(cpu_out,'w') as fd:
		fd.write('%s'%usage)

def MEM_analysis(allCont):
	usage={'TOTAL':[],'USED':[],'FREE':[],'CACHED':[]}
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	print nodeNum
	print timeLen
	for index in xrange(timeLen):
		mem_all= [ allCont[i][index]['SYSINFO']['CPUMEM']['MEM'] for i in xrange(nodeNum)]
		tmp = [0,0,0,0]
		for value in mem_all:
			for i,key in enumerate(usage.keys()):
				tmp[i] += prettyfloat(value[key])/prettyfloat(value['TOTAL'])
		for i,key in enumerate(usage.keys()):
			usage[key].append(tmp[i]/nodeNum)
	with open(mem_out,'w') as fd:
		fd.write('%s'%usage)

def NET_analysis(allCont):
	usage={'ETH5_IN':[],'ETH5_OUT':[]}
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	print nodeNum
	print timeLen
	for index in xrange(timeLen):
		net_all= [ allCont[i][index]['SYSINFO']['Network'] for i in xrange(nodeNum)]
		tmp = [0,0]
		for value in net_all:
			for i,key in enumerate(usage.keys()):
				tmp[i] += prettyfloat(value[key])
		for i,key in enumerate(usage.keys()):
			usage[key].append(tmp[i]/nodeNum)
	with open(net_out,'w') as fd:
		fd.write('%s'%usage)


def DISK_analysis(allCont):
	usage={'READ_SEC':[],'AVGQU_SZ':[],'READ_OPER':[],'AWAIT':[],'AVGRQ_SZ':[],'WRITE_OPER':[],'UTIL':[],'SVCTM':[],'WRITE_SEC':[]}
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	print nodeNum
	print timeLen
	for index in xrange(timeLen):
		disk_all= [ allCont[i][index]['SYSINFO']['DiskIO'] for i in xrange(nodeNum)]
		tmp = [0,0,0,0,0,0,0,0,0]
	#	pdb.set_trace()
		for value in disk_all:
			for i,key in enumerate(usage.keys()):
				# print value['DISK0'][key]
				# print value['DISK1'][key]
				# print value['DISK2'][key]
				ave = (prettyfloat(value['DISK0'][key])+prettyfloat(value['DISK1'][key])+prettyfloat(value['DISK2'][key]))/3
				tmp[i] +=ave

		for i,key in enumerate(usage.keys()):
			if key == 'UTIL':
				print tmp[i]/nodeNum
			usage[key].append((tmp[i])/nodeNum)
	with open(disk_out,'w') as fd:
		fd.write('%s'%usage)


def formalizeData(starttime, endtime,nodeCont):
	formalized=[]
	count = 0
	for i,t in enumerate(yieldTime(starttime,endtime)):
		pdict = yaml.load( nodeCont[count] )
		if convertDate(pdict['TIMESTAMP']) != t:
				tmp = {}
				tmp['HOST'] = pdict['HOST']
				tmp['SYSINFO'] = pdict['SYSINFO']
				formalized.append(tmp)
		else:
			del pdict['TIMESTAMP']
			formalized.append(pdict)
			count = count +1
	return formalized

sdate_obj=convertDate(starttime)
edate_obj=convertDate(endtime)

os.chdir(sourceFolder)
f = []
allCont = []

for (dirpath, dirnames, filenames) in os.walk('.'):
    f.extend(filenames)
    break
fhds = [open(filename) for filename in f]
print "format_data %s"%datetime.datetime.now()
for hd in fhds:
	nodeCont = hd.readlines()
	allCont.append(formalizeData(sdate_obj,edate_obj,nodeCont))

with open('formalized.txt') as fd:
	fd.write("%s"allCont)
print "start analysis %s"%datetime.datetime.now()


CPU_analysis(allCont)
MEM_analysis(allCont)
DISK_analysis(allCont)
NET_analysis(allCont)