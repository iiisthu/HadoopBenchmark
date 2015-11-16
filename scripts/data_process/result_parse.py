#import matplotlib.pyplot as plt
import os
import sys
import datetime
import subprocess
import pdb
import yaml
import pickle
#Mem Usage


sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/%s'%sys.argv[3]
outpath='%s/out'%sourceFolder
if not os.path.exists(outpath):
    os.makedirs(outpath)
cpu_out = '%s/cpu'%(outpath)
mem_out = '%s/mem'%(outpath)
disk_out = '%s/disk'%outpath
net_out= '%s/net'%outpath
host_out='%s/host'%outpath
starttime=sys.argv[1]
endtime=sys.argv[2]
option=sys.argv[3]
#maptime = sys.argv[4]
#reducetime=sys.argv[5]


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
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	print nodeNum
	print timeLen
	used=[]
	with open(cpu_out,'wb') as fd:
		for index in xrange(timeLen):
			used_all= [ 100-prettyfloat(allCont[i][index]['SYSINFO']['CPUMEM']['CPU']['IDLE']) for i in xrange(nodeNum)]
			used.append(used_all)
		pickle.dump(used,fd,-1)


def MEM_analysis(allCont):
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	used = []
	with open(mem_out,'wb') as fd:
		for index in xrange(timeLen):
			mem_all= [ prettyfloat(allCont[i][index]['SYSINFO']['CPUMEM']['MEM']['USED']) for i in xrange(nodeNum)]
			used.append(mem_all)
			#print mem_all
		pickle.dump(used,fd,-1)

def NET_analysis(allCont):
	usage={'ETH5_IN':[],'ETH5_OUT':[]}
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	bandwidth=[]
	with open(net_out,'wb') as fd:
		for index in xrange(timeLen):
			net_all= [ prettyfloat(allCont[i][index]['SYSINFO']['Network']['ETH5_IN']) + 
			prettyfloat(allCont[i][index]['SYSINFO']['Network']['ETH5_OUT']) for i in xrange(nodeNum)]
			bandwidth.append(net_all)
		pickle.dump(bandwidth,fd,-1)

def DISK_analysis(allCont):
	usage={}
	nodeNum = len(allCont)
	timeLen = len(allCont[0])
	bandwidth=[]
	oneList=[]
	twoList=[]
	threeList=[]
	with open(disk_out,'wb') as fd:
		for index in xrange(timeLen):
			# disk_all= [ (prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK0']['READ_SEC'])+
			# 			prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK0']['WRITE_SEC'])+
			# 			prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK1']['READ_SEC'])+
			# 			prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK1']['WRITE_SEC'])+
			# 			prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK2']['READ_SEC'])+
			# 			prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK2']['WRITE_SEC'])
			# 			)/2 for i in xrange(nodeNum)]
			disk_all = [(prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK0']['MBWRITE'])+
				prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK0']['MBREAD'])+
					prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK1']['MBWRITE'])+
				prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK1']['MBREAD'])+
					prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK2']['MBWRITE'])+
				prettyfloat(allCont[i][index]['SYSINFO']['DiskIO']['DISK2']['MBREAD'])) for i in xrange(nodeNum)]
			bandwidth.append(disk_all)
		nodeList=[ allCont[i][0]['HOST'] for i in xrange(nodeNum)]
		pickle.dump(bandwidth, fd, -1)
		hd = open(host_out,'wb')
		pickle.dump(nodeList,hd,-1)
		hd.close()

def formalizeData(starttime, endtime,nodeCont,index):
	formalized=[]
	count = 0
	length= len(nodeCont)
	#print length
	for i,t in enumerate(yieldTime(starttime,endtime)):

		if count >= length:
			pdict = yaml.load(nodeCont[length-1])
		else: 
		#	print count
			pdict = yaml.load( nodeCont[count] )
		if convertDate(pdict['TIMESTAMP'])< starttime:
			count = count + 1
			pdict = yaml.load( nodeCont[count] )
		# if index == 2:
		# 	pdb.set_trace()
		if convertDate(pdict['TIMESTAMP']) != t:
		#		print 'Leak'
				tmp = {}
				#tmp['TIMESTAMP'] = t.strftime("%Y-%m-%d %H:%M:%S")
				tmp['HOST'] = pdict['HOST']
				tmp['SYSINFO'] = pdict['SYSINFO']
				formalized.append(tmp)
		else:
			del pdict['TIMESTAMP']
			formalized.append(pdict)
			count = count +1

	print len(formalized)
	#print formalized[0]['TIMESTAMP']

	return formalized

sdate_obj=convertDate(starttime)
edate_obj=convertDate(endtime)

os.chdir(sourceFolder)
f = []
allCont = []

for (dirpath, dirnames, filenames) in os.walk('.'):
    f.extend(filenames)
    break
# print '%s'%f
# pdb.set_trace()
fhds = [open(filename) for filename in f]
print "format_data %s"%datetime.datetime.now()
for i,hd in enumerate(fhds):
	nodeCont = hd.readlines()
	# print nodeCont
	# pdb.set_trace()
	allCont.append(formalizeData(sdate_obj,edate_obj,nodeCont,i))

with open('%s/formalized.txt'%outpath,'w') as fd:
	fd.write("%s"%allCont)
print "start analysis %s"%datetime.datetime.now()

# def plotCPU(allCont):
# 	nodeNum = len(allCont)
# 	timeLen = len(allCont[0])
# 	x = []
# 	y = []
# 	z = []
# 	for index in xrange(timeLen):
#  		cpu_all= [ allCont[i][index]['SYSINFO']['CPUMEM']['CPU'] for i in xrange(nodeNum)]
#  		used=[1-prettyfloat(cpu['IDLE']) for cpu in cpu_all]
#  		sorted_data = np.sort(data)
# 		yvals=np.arange(len(sorted_data))/float(len(sorted_data))
# 		x.append(sorted_data)
# 		y.append(yvals)
# 		z.append(index*5)
# 	fig = plt.figure()
# 	ax = plt.axes(projection='3d')
# 	ax.plot_surface(x, y, z, cmap=plt.cm.jet, rstride=1, cstride=1, linewidth=0)

# plotCPU()

CPU_analysis(allCont)
MEM_analysis(allCont)
DISK_analysis(allCont)
NET_analysis(allCont)