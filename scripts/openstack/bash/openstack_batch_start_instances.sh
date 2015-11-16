#!/bin/bash

images=$(nova list | grep shenh10 | cut -d' ' -f2)
for image in $images;do
 echo $image 
 nova start $image
done
