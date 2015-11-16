
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import yaml
import sys
import os
import datetime
sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts'
start = [13191,16147,17255,17733,18393,18934]
end = [15469,17236,17721,18028,18829,28033]

mydata = '%s/ready.txt'%sourceFolder

class prettyfloat(float):
        def __repr__(self):
                return "%0.2f" % self

def plotCPU(allCont):
	usage={'USR':[],'SYS':[],'IOWAIT':[],'IDLE':[]}
	timeLen = len(allCont)
	#print timeLen
	for index in xrange(timeLen):
			cpu_all=  allCont[index]['SYSINFO']['CPUMEM']['CPU'] 
			for i,key in enumerate(usage.keys()):
				usage[key].append(prettyfloat(cpu_all[key]))
	cpu = usage
	#print cpu
	length = len(cpu['SYS'])
	x = np.linspace(1, length, length)
	y = np.row_stack((cpu['USR'],cpu['SYS'],cpu['IOWAIT']))

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	plt.axis([0.0,timeLen, 0,100])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	entry = ['USR','SYS','IOWAIT']
	colors = ['r','b','yellow','gold','k']
	ax.stackplot(x, y,colors=(colors))
	plt.title('CPU Occupation - 1 day', fontdict=font)
	plt.xlabel('time (5s)', fontdict=font)
	plt.ylabel('Occupation Percent(%)', fontdict=font)
	for t in start:
		if t < timeLen:
			plt.axvline(t,hold=None,label="Start",color='black',linestyle="--")
	for t in end:
		if t < timeLen:
			plt.axvline(t,hold=None,label="End",color='red',linestyle="--")

	p = []
	for i,label in enumerate(entry):
		p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	ax.legend(p, entry)
	# red_patch = mpatches.Patch(color='r', label='USER')
	# orange_patch = mpatches.Patch(color='orangered', label='SYS')
	# yellow_patch = mpatches.Patch(color='yellow',label='IOWAIT')
	# plt.legend(handles=[red_patch])
	plt.show()


def plotMem(allCont):
	usage={'TOTAL':[],'USED':[],'FREE':[],'CACHED':[]}
	timeLen = len(allCont)
	for index in xrange(timeLen):
			mem_all=  allCont[index]['SYSINFO']['CPUMEM']['MEM'] 
			for i,key in enumerate(usage.keys()):
				usage[key].append(prettyfloat(mem_all[key])/prettyfloat(mem_all['TOTAL']))

	mem = usage
	length = len(mem['TOTAL'])
	x = np.linspace(1, length, length)
	y = np.row_stack((mem['USED'],mem['CACHED'],mem['FREE']))

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	plt.axis([0.0,timeLen, 0,1])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	entry = ['USED','CACHED','FREE']
	colors = ['r','b','yellow','gold','k']
	ax.stackplot(x, y,colors=(colors))
	plt.title('RAM Occupation - 1 day', fontdict=font)
	plt.xlabel('time (5s)', fontdict=font)
	plt.ylabel('Occupation Ratio', fontdict=font)
	for t in start:
		if t < timeLen:
			plt.axvline(t,hold=None,label="Start",color='black',linestyle="--")
	for t in end:
		if t < timeLen:
			plt.axvline(t,hold=None,label="End",color='red',linestyle="--")

	p = []
	for i,label in enumerate(entry):
		p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	ax.legend(p, entry)	
	plt.show()

def plotDisk(disk):
	#usage={'READ_SEC':[],'AVGQU_SZ':[],'READ_OPER':[],'AWAIT':[],'AVGRQ_SZ':[],'WRITE_OPER':[],'UTIL':[],'SVCTM':[],'WRITE_SEC':[]}
	usage={'READ_SEC':[],'WRITE_SEC':[],'UTIL':[]}
	timeLen = len(allCont)
	#print timeLen
	for index in xrange(timeLen):
		disk_all= allCont[index]['SYSINFO']['DiskIO'] 
	#	pdb.set_trace()
		for i,key in enumerate(usage.keys()):
			# print value['DISK0'][key]
			# print value['DISK1'][key]
			# print value['DISK2'][key]
			ave = (float(disk_all['DISK0'][key])+float(disk_all['DISK1'][key])+float(disk_all['DISK2'][key]))/3
			usage[key].append(ave)
	#print usage
	disk = usage
	length = len(disk['READ_SEC'])
	x = np.linspace(1, length, length)

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
   	colors = ['r','b','yellow','gold','k']

	fig, ax = plt.subplots()
	# plt.axis([0.0,timeLen, 0,100])
	# ax = plt.gca()
	# ax.set_autoscale_on(False)
	#entry = ['UTIL']
	ax.plot(x, list(np.array(disk['READ_SEC'])+np.array(disk['WRITE_SEC'])))
	plt.title('DISK IO Bandwidth - 1 day', fontdict=font)
	plt.xlabel('time (5s)', fontdict=font)
	plt.ylabel('IO Bandwidth(KB/s)', fontdict=font)
	for t in start:
		if t < timeLen:
			plt.axvline(t,hold=None,label="Start",color='black',linestyle="--")
	for t in end:
		if t < timeLen:
			plt.axvline(t,hold=None,label="End",color='red',linestyle="--")	
	plt.show()

	fig, ax = plt.subplots()
	plt.axis([0.0,timeLen, 0,100])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	#entry = ['UTIL']
	ax.plot(x, disk['UTIL'])
	plt.title('DISK Utilization - 1 day', fontdict=font)
	plt.xlabel('time (5s)', fontdict=font)
	plt.ylabel('Percentage(%)', fontdict=font)
	for t in start:
		if t < timeLen:
			plt.axvline(t,hold=None,label="Start",color='black',linestyle="--")
	for t in end:
		if t < timeLen:
			plt.axvline(t,hold=None,label="End",color='red',linestyle="--")	
	plt.show()


def plotNet(allCont):
	usage={'ETH5_IN':[],'ETH5_OUT':[]}
	timeLen = len(allCont)
	for index in xrange(timeLen):
			net_all=  allCont[index]['SYSINFO']['Network'] 
			for i,key in enumerate(usage.keys()):
				usage[key].append(prettyfloat(net_all[key]))
	net = usage
	length = len(net['ETH5_IN'])
	x = np.linspace(1, length, length)

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	#plt.xlim([0.0,3000])
	#ax = plt.gca()
	#ax.set_autoscale_on(False)
	y = [ (prettyfloat(eth5_in)+prettyfloat(eth5_out)) for eth5_in, eth5_out in zip(net['ETH5_IN'],net['ETH5_OUT'])]
	#print y
	#entry = ['UTIL']
	colors = ['r','b','yellow','gold','k']
	ax.plot(x ,y)
	plt.title('Network Bandwidth - 1 day', fontdict=font)
	plt.xlabel('time (5s)', fontdict=font)
	plt.ylabel('Bandwidth(KB/s)', fontdict=font)
	for t in start:
		if t < timeLen:
			plt.axvline(t,hold=None,label="Start",color='black',linestyle="--")
	for t in end:
		if t < timeLen:
			plt.axvline(t,hold=None,label="End",color='red',linestyle="--")	
	# p = []
	# for i,label in enumerate(entry):
	# 	p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	# ax.legend(p, entry)	
	plt.show()





f = []



print "format_data %s"%datetime.datetime.now()
allCont = []
with open(mydata) as fd:
	lines = fd.readlines()
	allCont =[ yaml.load(line) for line in lines]

#print allCont
print "start analysis %s"%datetime.datetime.now()
plotCPU(allCont)
plotMem(allCont)
plotNet(allCont)
plotDisk(allCont)
