from fabric import tasks,state
from fabric.api import *
import sys
from fabric.contrib.files import *
filename="/hdfs/data1/test/hadoop_src/etc/hadoop/slaves"
env.hosts=[line for line in open(filename)]
if len(sys.argv) < 3:
	print 'usage: python fabric.py  [interval] [date:hour:minute]  '
	sys.exit()


interval = sys.argv[1]
starttime = sys.argv[2]
# No need to decorate this function with @task
@parallel
def worker():
     run('python /home/shenh10/system_monitor/collect_data.py %s %s %s'%(env.host, interval, starttime))

def main():
    print state.output
    tasks.execute(worker)

if __name__ == '__main__':
    main()
