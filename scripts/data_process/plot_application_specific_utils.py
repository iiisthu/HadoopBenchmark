# import matplotlib.pyplot as plt




import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import yaml
import sys
sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/%s/out'%sys.argv[1]
cpu_in = '%s/cpu'%sourceFolder
mem_in = '%s/mem'%sourceFolder
disk_in = '%s/disk'%sourceFolder
net_in='%s/net'%sourceFolder


case = sys.argv[2]
with open(cpu_in) as fd:
	cpu=yaml.load(fd.readline())
with open(mem_in) as fd:
	mem=yaml.load(fd.readline())
with open(net_in) as fd:
	net=yaml.load(fd.readline())
with open(disk_in) as fd:
	disk=yaml.load(fd.readline())

class prettyfloat(float):
        def __repr__(self):
                return "%0.2f" % self

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

def plotCPU(cpu):
	length = len(cpu['SYS'])
	x = np.linspace(1, length*5, length)
	y = np.row_stack((cpu['USR'],cpu['SYS'],cpu['IOWAIT']))

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	plt.axis([0.0,len(x), 0,1])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	entry = ['USR','SYS','IOWAIT']
	colors = ['r','b','yellow','gold','k']
	ax.stackplot(x, y,colors=(colors))
	plt.title('Node Average CPU Occupation-wordcount 10T- %s '%case, fontdict=font)
	plt.xlabel('time (s)', fontdict=font)
	plt.ylabel('Occupation Percent(%)', fontdict=font)
	p = []
	for i,label in enumerate(entry):
		p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	ax.legend(p, entry)
	# red_patch = mpatches.Patch(color='r', label='USER')
	# orange_patch = mpatches.Patch(color='orangered', label='SYS')
	# yellow_patch = mpatches.Patch(color='yellow',label='IOWAIT')
	# plt.legend(handles=[red_patch])
	plt.show()

def plotMem(mem):
	length = len(mem['TOTAL'])
	x = np.linspace(1, length*5, length)
	y = np.row_stack((mem['USED'],mem['CACHED'],mem['FREE']))

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	plt.axis([0.0,len(x), 0,1])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	entry = ['USED','CACHED','FREE']
	colors = ['r','b','yellow','gold','k']
	ax.stackplot(x, y,colors=(colors))
	plt.title('Node Average RAM Occupation-wordcount 10T-%s'%case, fontdict=font)
	plt.xlabel('time (s)', fontdict=font)
	plt.ylabel('Occupation Percent(%)', fontdict=font)
	p = []
	for i,label in enumerate(entry):
		p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	ax.legend(p, entry)	
	plt.show()

def plotDisk(disk):
	length = len(disk['UTIL'])
	x = np.linspace(1, length*5, length)

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	plt.axis([0.0,len(x), 2000,8000])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	#entry = ['UTIL']
	colors = ['r','b','yellow','gold','k']
	all_io = list(np.array(disk['READ_SEC'])+np.array(disk['WRITE_SEC']))
	print all_io
	ax.plot(x, all_io)
	plt.title('Node Average Disk IO Bandwidth-wordcount 10T-%s'%case, fontdict=font)
	plt.xlabel('time (s)', fontdict=font)
	plt.ylabel('Bandwidth (KB/s))', fontdict=font)
	# p = []
	# for i,label in enumerate(entry):
	# 	p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	# ax.legend(p, entry)	
	plt.show()

def plotNet(net):
	length = len(net['ETH5_IN'])
	x = np.linspace(1, length*5, length)

	font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
	fig, ax = plt.subplots()
	plt.axis([0.0,len(x),0,150000])
	ax = plt.gca()
	ax.set_autoscale_on(False)
	y = [ (prettyfloat(eth5_in)+prettyfloat(eth5_out)) for eth5_in, eth5_out in zip(net['ETH5_IN'],net['ETH5_OUT'])]
	print y
	#entry = ['UTIL']
	colors = ['r','b','yellow','gold','k']
	ax.plot(x ,y)
	plt.title('Node Average Network Bandwidth 10T-%s'%case, fontdict=font)
	plt.xlabel('time (s)', fontdict=font)
	plt.ylabel('Bandwidth(KB/s)', fontdict=font)
	# p = []
	# for i,label in enumerate(entry):
	# 	p.append(mpatches.Rectangle((0, 0), 1, 1, fc=colors[i]))
	# ax.legend(p, entry)	
	plt.show()

# fnx = lambda : np.random.randint(5, 50, 10)
# y = np.row_stack((fnx(), fnx(), fnx()))
# x = np.arange(10)

# y1, y2, y3 = fnx(), fnx(), fnx()

# fig, ax = plt.subplots()
# ax.stackplot(x, y)
# plt.show()

plotCPU(cpu)
plotMem(mem)

plotDisk(disk)
plotNet(net)





# fig, ax = plt.subplots()
# ax.stackplot(x, y1, y2, y3)
# plt.show()
# x = cpu['SYS']
# x1 = np.linspace(0.0, len(x), len(x))
# print x1
# y1 = x

# plt.plot(x1, y1, 'k')
# plt.title('Damped exponential decay', fontdict=font)
# plt.text(2, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict=font)
# plt.xlabel('time (s)', fontdict=font)
# plt.ylabel('voltage (mV)', fontdict=font)

# # Tweak spacing to prevent clipping of ylabel
# plt.subplots_adjust(left=0.15)
# plt.show()