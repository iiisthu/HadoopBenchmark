import matplotlib.pyplot as plt
import numpy as np

sourceFolder='/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts/count_result'

count_list = []
with open(sourceFolder) as fd:
	lines = fd.readlines()
	for line in lines:
		count_list.append(int((line.split(' '))[4].strip()))


font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

fig, ax = plt.subplots()
nodeNum = len(count_list)
ind = np.arange(nodeNum)
width = 0.9 

rects1 = ax.bar(ind, count_list, width, color='r',label='Number of VMs')
plt.ylim([0,8])
ax = plt.gca()
ax.set_autoscale_on(False)
plt.title('Virtual Machine Allocation ', fontdict=font)
plt.xlabel('Nodes', fontdict=font)
plt.ylabel('Number of VMs', fontdict=font)
ax.legend()
plt.show()