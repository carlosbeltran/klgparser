import numpy as np
import cv2
import zlib
import Image

f = open("August Exp/2017-08-01.00.klg", "rb")
byte = f.read(4)
a=map(ord,byte)
numberofframes= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]
count=0
depth=np.ones( (480,640),  dtype=np.uint16)
rgb=np.ones((480, 640, 3), dtype=np.uint8)
while count<numberofframes:
        print count
	byte = f.read(8)
	a=map(ord,byte)
	#print a
	byte = f.read(4)
	a=map(ord,byte)
	#print a
	depthsize= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]
	byte = f.read(4)
	a=map(ord,byte)
	#print depthsize
	imagesize= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]
	byte = f.read(depthsize)
        if(count%37==0):
             dimage=zlib.decompress(byte)
	     a=map(ord,dimage)
	     for i in range(len(a)-1):
             	depth[(i/1280)][(i%1280)/2]=a[i+1]*256+a[i]
	     dname="klg2png_output/depth_aug/depth_aug"+str(count)+".png"
	     cv2.imwrite(dname,depth)
	byte = f.read(imagesize)
	#print timage.shape
        if(count%37==0): 
             timage = np.fromstring(byte, dtype=np.uint8)
             rgb=cv2.imdecode(timage,1)
	     cname="klg2png_output/rgb_aug/rgb_aug"+str(count)+".png"
	     cv2.imwrite(cname,cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))
	count+=1
f.close()
