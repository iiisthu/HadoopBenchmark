import sys

startTime=sys.argv[1]

endTime=sys.argv[2]


mapStart=sys.argv[3]
mapEnd = sys.argv[4]

redStart=sys.argv[5]

redEnd=sys.argv[6]

shuffleEnd=sys.argv[7]


def timeToSec(timestr):
	arr = timestr.split(':')
	sec = int(arr[0])*60*60+ int(arr[1])*60+int(arr[2])
	return sec



totalDuration=timeToSec(endTime) - timeToSec(startTime)
print 'Total Duration: %s s'%totalDuration

points = totalDuration/5 
print 'Total points: %s'%(points)

mapDuration=timeToSec(mapEnd) - timeToSec(mapStart)

print 'Map Duration: %s s' %mapDuration

print 'Map Start Point: %s'%((timeToSec(mapStart)-timeToSec(startTime)+1)/5)
print 'Map End Point: %s' %((timeToSec(mapEnd)-timeToSec(startTime)+1)/5)

redDuration=timeToSec(redEnd) - timeToSec(redStart)+1
shuffleDuration = timeToSec(shuffleEnd) - timeToSec(redStart)+1

print 'Shuffle Duration: %s s'%shuffleDuration

print 'Reduce Duration: %s s'%redDuration

print 'Reduce Start Point: %s '%((timeToSec(redStart)-timeToSec(startTime)+1)/5)

print 'Shuffle End Point: %s ' %((timeToSec(shuffleEnd)-timeToSec(startTime)+1)/5)

print 'Reduce End Point: %s' %((timeToSec(redEnd)-timeToSec(startTime)+1)/5)

