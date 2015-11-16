import matplotlib.pyplot as plt
import numpy as np

sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/'


vm_sort=[[4858,5231,4576],[778.67,897,695],[125.67,136,118]]
vm_word=[[3228.33,3290,3195],[690.67,708,669],[153.33,165,143]]
docker_sort=[[3681,3882,3537],[939.33,955,913],[120.33,123,118]]
docker_word=[[3786,3855,3725],[1298.67,1571,1152],[217,281,165]]

phy_sort=[[2831.75,2893,2758],[1580.333333,1744,1311],[114.3333333,122,110]]
phy_word=[[4409,4738,4111],[1183.666667,1227,1129],[279,271,288]]

vm_io=[[93.758,80.85],[182.163,80.388],[204.56,95.61],[354.509,155.144]]
docker_io=[[62.605,52.523],[452.80,92.91],[290.97,96.38],[508.82,157.84]]
phy_io=[[22.34,18.01],[85.70,38.92],[225.69,144.16],[260.44,187.53]]

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

def parseStruct(array):
	arr = np.asarray
	val=arr([ [array[i][0]] for i in xrange(len(array))]).flatten()
	err=arr([[np.abs(array[i][1]-array[i][0]),np.abs(array[i][2]-array[i][0])] for i in xrange(len(array))]).T	
	return [val, err]

def plotDuration(vm_data, docker_data,phy_data,case):
	fig, ax = plt.subplots()
	ind = np.arange(3)
	width = 0.3
	print ind
	[val_vm, err_vm]=parseStruct(vm_data)
	[val_docker, err_docker]=parseStruct(docker_data)
	[val_phy, err_phy]=parseStruct(phy_data)
	rects1 = ax.bar(ind,val_vm , width, color='r',label='VM',yerr=np.array(err_vm))
	rects2 = ax.bar(ind+width,val_docker , width, color='b',label='Docker',yerr=np.array(err_docker))
	rects3 = ax.bar(ind+width*2,val_phy , width, color='y',label='Physical',yerr=np.array(err_phy))

	# plt.ylim([0,8])
	# ax = plt.gca()
	# ax.set_autoscale_on(False)
	ax.set_xticks(ind+width)
	ax.set_xticklabels( ('5T','1T','100G') )
	plt.title('%s Execution Time - 3 cases'%case, fontdict=font)
	plt.xlabel('Input Size', fontdict=font)
	plt.ylabel('Duration(s)', fontdict=font)
	ax.legend()
	plt.show()

def parseBwd(array):
	read = [array[i][0] for i in xrange(len(array))]
	write = [array[i][1] for i in xrange(len(array))]
	return [read,write]

def plotBandwidth(vm_data,docker_data,phy_data):
	fig, ax = plt.subplots()
	ind = np.arange(4)
	width = 0.3
	[vm_read,vm_write]=parseBwd(vm_data)
	[docker_read,docker_write]=parseBwd(docker_data)
	[phy_read,phy_write]=parseBwd(phy_data)
	ax.plot(ind,vm_read ,color='r',label='VM Read')
	ax.plot(ind,vm_write,'--' ,color='r',label='VM Write')
	ax.plot(ind,docker_read ,color='b',label='Docker Read')
	ax.plot(ind,docker_write,'--' ,color='b',label='Docker Write')
	ax.plot(ind,phy_read ,color='y',label='Physical Read')
	ax.plot(ind,phy_write,'--' ,color='y',label='Physical Write')
	# plt.ylim([0,8])
	# ax = plt.gca()
	# ax.set_autoscale_on(False)
	ax.set_xticks(ind)
	ax.set_xticklabels( ('10T','1T','100G','10G') )
	plt.title('Disk IO Speed - 3 cases', fontdict=font)
	plt.xlabel('Input Size', fontdict=font)
	plt.ylabel('Bandwidth(MB/s)', fontdict=font)
	ax.legend()
	plt.show()

plotDuration(vm_sort,docker_sort,phy_sort,'Sort')
plotDuration(vm_word,docker_word,phy_word,'WordCount')
plotBandwidth(vm_io,docker_io,phy_io)
