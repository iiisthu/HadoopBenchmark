import os
import sys
import yaml
import datetime
import subprocess
import pdb
import linecache
home = '/Users/shenh10/Documents/CodingPath/GraduationThesis/scripts'
sourceFolder='%s/data'%(home)

starttime=sys.argv[1]
endtime=sys.argv[2]
outpath='%s/%s'%(home,sys.argv[3])

# [s_date,s_hour,s_minute,s_second] = starttime.split(':')
# [e_date,e_hour,e_minute,e_second] = endtime.split(':')
sdate_obj=datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
edate_obj=datetime.datetime.strptime(endtime,"%Y-%m-%d %H:%M:%S")
if not os.path.exists(outpath):
    os.makedirs(outpath)
interval = 5
def totalseconds(td):
        return 1+(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


def count_lines(stime,etime):
	if etime < stime:
		return -1
	est_lines=totalseconds(etime-stime)/5
	return est_lines

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def writefile(startPos,endPos,infile,outfile):
	print infile
	print outfile
	commands = ['sed', '-n', '%d,%dp'%(startPos,endPos),'%s'%infile]
	print commands
	p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result, err = p.communicate()
	fd = open(outfile,'w')
	fd.write(result)
	fd.close()
	# if p.returncode != 0:
	# 	raise IOError(err)

def seekStartTime(fname, flen, stime,step,pos):
	line = linecache.getline(fname,pos)
	pdict = yaml.load(line)
	curtime=datetime.datetime.strptime(pdict['TIMESTAMP'],"%Y-%m-%d %H:%M:%S")
	if curtime < stime:
		step=step*2
		return seekStartTime(fname,flen,stime,step,min([flen,pos+step]))
	elif curtime == stime:
		return pos
	else:
		step=step/2
		return seekStartTime(fname,flen,stime,step,max([0,pos-step]))
os.chdir(sourceFolder)
f = []

for (dirpath, dirnames, filenames) in os.walk('.'):
    f.extend(filenames)
    break
for filename in f:
	filePath='%s/%s'%(sourceFolder,filename)
	fileLen=file_len(filePath)
	starts=seekStartTime(filePath,fileLen,sdate_obj,1,1)
	ends=seekStartTime(filePath,fileLen,edate_obj,1,starts)
	#ends=starts+count_lines(sdate_obj,edate_obj)
	if ends< starts:
		print "Ends < Starts! exit"
		sys.exit(1)
	endEntry=yaml.load(linecache.getline(filePath,ends))
	print "Start line : %s, End line: %s"%(starts,ends)
	print "File %s : parsed endtime: %s, expected endtime: %s"%(endEntry['HOST'],endEntry['TIMESTAMP'],endtime)
	outfile = '%s/%s'%(outpath,filename)
	writefile(starts,ends,'%s/%s'%(sourceFolder, filename),'%s/%s'%(outpath,filename))	
