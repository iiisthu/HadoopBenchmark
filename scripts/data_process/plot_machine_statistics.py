# import matplotlib.pyplot as plt




import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as lines
import yaml
import sys
import pdb
import datetime
import pickle
import os

class prettyfloat(float):
        def __repr__(self):
                return "%0.2f" % self

sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/%s/out'%sys.argv[1]
output = '/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/pics/%s'%sys.argv[1]
cpu_in = '%s/cpu'%sourceFolder
mem_in = '%s/mem'%sourceFolder
disk_in = '%s/disk'%sourceFolder
net_in='%s/net'%sourceFolder
host_in='%s/host'%sourceFolder

print "Start load %s..."%datetime.datetime.now()
case = sys.argv[2]
if not os.path.exists(output):
    os.makedirs(output)

PhaseStr=sys.argv[3]
PhaseArr =[ int(i)*5 for i in PhaseStr.split(':')]

with open(cpu_in,'rb') as fd:
	cpu=pickle.load(fd)

with open(mem_in,'rb') as fd:
	mem=pickle.load(fd)

with open(net_in,'rb') as fd:
	net=pickle.load(fd)
with open(disk_in,'rb') as fd:
	disk=pickle.load(fd)

with open(host_in,'rb') as fd:
	host=pickle.load(fd)

print "Finish load %s..."%datetime.datetime.now()


class prettyfloat(float):
        def __repr__(self):
                return "%0.2f" % self

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }


def plotMajorFeature(value,feature,ylabel):
	nodeNum = len(value[0])
	timeLen = len(value)
	fig ,ax = plt.subplots()
	middles=[]
	aves=[]
	x = np.linspace(1, timeLen*5, timeLen)
	for index in xrange(timeLen):
 		sorted_data = np.sort(value[index])
 		middle=sorted_data[len(sorted_data)/2]
 		ave=np.mean(sorted_data)
 		aves.append(ave)
		middles.append(middle)
	ax.plot(x,middles,label='Middle Value')
	ax.plot(x,aves,label='Average Value')
	plt.title('%s - %s '%(feature,case), fontdict=font)
	plt.xlabel('time (s)', fontdict=font)
	plt.ylabel('%s'%ylabel, fontdict=font)

	colors = ['red','black','y','green','blue']
	labels = [ "Map Start","Map End","Reduce Start" ,"Reduce Done","Shuffle Done"]
	for i in xrange(len(PhaseArr)):
		plt.axvline(PhaseArr[i],hold=None,label=labels[i],color=colors[i],linestyle="--")
	# l = []
	# for i,label in enumerate(labels):
	# 	l.append(lines.Line2D(null,null,linestyle='--',color=colors[i]))
	box = ax.get_position()
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.79, box.height])

# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	fig.savefig('%s/%s_%s.png'%(output,feature.replace(' ','_'),'mid_ave'))
	plt.close(fig)


def plotConcurrentFeature(value,feature,ylabel):
	nodeNum = len(value[0])
	timeLen = len(value)
	x = np.linspace(1, timeLen*5, timeLen)
	fig, ax = plt.subplots()
	for index in xrange(nodeNum):
		node = [ value[i][index] for i in xrange(timeLen)]
		ax.plot(x, node)
	plt.title('%s - %s '%(feature,case), fontdict=font)
	plt.xlabel('time (s)', fontdict=font)
	plt.ylabel('%s'%ylabel, fontdict=font)

	colors = ['red','black','y','green','blue']
	labels = [ "Map Start","Map End","Reduce Start" ,"Reduce Done","Shuffle Done"]
	for i in xrange(len(PhaseArr)):
		plt.axvline(PhaseArr[i],hold=None,label=labels[i],color=colors[i],linestyle="--")
	# l = []
	# for i,label in enumerate(labels):
	# 	l.append(lines.Line2D(null,null,linestyle='--',color=colors[i]))
	box = ax.get_position()
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.79, box.height])

# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	fig.savefig('%s/%s_%s.png'%(output,feature.replace(' ','_'),'all'))
	plt.close(fig)

def inRange(value,rangeStart, rangeEnd):
	if value <= rangeEnd and value >= rangeStart:
		return True;
	return False

def yieldId(id_start, id_end):
	id = id_start
	while id <= id_end:
		yield id
		id = id + 1

def bandwidthPerNode(value, feature,ylabel):
	nodeNum = len(value[0])
	timeLen = len(value)
	x = np.linspace(1, nodeNum , nodeNum)
	nodes_map=[0]*nodeNum
	nodes_red=[0]*nodeNum
	nodes_shuffle=[0]*nodeNum
	nodes_map_max=[0]*nodeNum
	nodes_map_min=[0]*nodeNum
	nodes_red_std=[0]*nodeNum
	nodes_shuffle_std=[0]*nodeNum
	fig, ax = plt.subplots()
	id = [ item/5 for item in PhaseArr ]
	for node in xrange(nodeNum):
			# nodes_map[node] = np.mean([value[i][node] for i in yieldId(id[0],id[1])])
			# nodes_red[node] = np.mean([value[i][node] for i in yieldId(id[2],id[3])])
			# nodes_shuffle[node] = np.mean([value[i][node] for i in xrange(id[2],id[4])])
		print len(value)
		map_list=[ value[id[0]:id[1]][i][node] for i in xrange(id[1]-id[0]) ] 
		red_list = [ value[id[2]:id[3]][i][node] for i in xrange(id[3]-id[2])  ]
		shuffle_list = [ value[id[2]:id[4]][i][node] for i in xrange(id[4]-id[2])  ] 
		nodes_map[node] = np.mean(map_list )
		#print 'Host: [%s] ; Map mean : %s Value: %s'%(host[node],nodes_map[node],map_list)
		nodes_red[node] = np.mean(red_list)
		#nodes_red_std[node] = np.std(value[id[2]:id[3]][node])
		nodes_shuffle[node] = np.mean( shuffle_list )
		#nodes_shuffle_std[node] = np.std(value[id[2]:id[4]][node])
	ind = np.arange(nodeNum)
	width = 0.35       # the width of the bars
	rects1 = ax.bar(ind-width, nodes_map, width, color='r',label='Map Phase')
	rects2 = ax.bar(ind+width, nodes_red, width, color='y', label='Reduce Phase')
	rects3 = ax.bar(ind, nodes_shuffle, width, color='b', label='Shuffle Phase')
# 	print x
# 	print nodes_red
# 	ax.plot(x, nodes_map, label='map')
# 	ax.plot(x, nodes_red,label='reduce')
# 	ax.plot(x, nodes_shuffle,label='shuffle')
	for i,val in enumerate(nodes_map):
		if  val < 10:
			print host[i]
	plt.xlim([-width,nodeNum+width])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	plt.title('%s - %s '%(feature,case), fontdict=font)
	plt.xlabel('Nodes', fontdict=font)
	plt.ylabel('%s'%ylabel, fontdict=font)
	ax.legend()
	fig.savefig('%s/%s_%s.png'%(output,feature.replace('/'," Per ").replace(' ','_'),'bd'))
	plt.close(fig)

# 	# l = []
# 	# for i,label in enumerate(labels):
# 	# 	l.append(lines.Line2D(null,null,linestyle='--',color=colors[i]))
# 	box = ax.get_position()
# 	box = ax.get_position()
# 	ax.set_position([box.x0, box.y0, box.width * 0.79, box.height])

# # Put a legend to the right of the current axis
# 	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# 	plt.show()
plotConcurrentFeature(disk,'Disk IO Speed','Bandwidth(MB/s)')
plotConcurrentFeature(net,'Network Bandwidth','Bandwidth(KB/s)')
plotConcurrentFeature(cpu, 'CPU Occupation', 'Percentage(%)')
plotConcurrentFeature(mem, 'Memory Occupation', 'Memory Usage(MB)')
plotMajorFeature(cpu,'CPU Occupation', 'Percentage(%)')
plotMajorFeature(disk,'Disk IO Speed','Bandwidth(MB/s)')
plotMajorFeature(net,'Network Bandwidth','Bandwidth(KB/s)')
plotMajorFeature(mem, 'Memory Occupation', 'Memory Usage(MB)')
bandwidthPerNode(net,'Average Network Bandwidth/Node','Bandwidth(KB/s)')
bandwidthPerNode(disk,'Average Disk IO Speed/Node','Bandwidth(MB/s)')


