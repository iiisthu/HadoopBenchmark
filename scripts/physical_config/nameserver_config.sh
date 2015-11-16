#/bin/bash


for i in `seq 1 9`;do
   sudo echo "$i.0.6  IN  PTR  vp00$i.2.iiis.co.;" >> /var/named/10
done
for i in `seq 10 99`;do
   sudo echo "$i.0.6  IN  PTR  vp0$i.2.iiis.co.;" >> /var/named/10
done
for i in `seq 100 125`;do
   sudo echo "$i.0.6  IN  PTR  vp$i.2.iiis.co.;" >> /var/named/10
done
