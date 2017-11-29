#!/usr/bin/python

'''
    File name: klgparser.py
    Based on code by Neil Ibrahimli
'''
__author__     = "Carlos Beltran-Gonzalez"
__copyright__  = "Copyright 2017, Carlos Beltran-Gonzalez"
__credits__    = "Neil Ibrahimli"
__licence__    = "GPL"
__version__    = "3.0"
__maintainer__ = "Carlos Beltran-Gonzalez"
__email__      = "carlos.beltran@iit.it"

import numpy as np
import cv2
import zlib
import Image
import filecmp
import unittest
import os
import shutil

class TestKLGParser(unittest.TestCase):
    def testDepthOutput(self):
        outputfolder = "klg2png_output/depth_aug/" 
        testfolder   = "output_test/"
        for indx in range(10):
            filename = "depth_aug" + str(indx) +".png"
            file1 = outputfolder + filename
            file2 = testfolder   + filename
            self.assertTrue(filecmp.cmp(file1,file2,shallow=False))
    def testRGBOutput(self):
        outputfolder = "klg2png_output/rgb_aug/"
        testfolder   = "output_test/"
        for indx in range(10):
            filename = "rgb_aug" + str(indx) + ".png"
            file1 = outputfolder + filename
            file2 = testfolder   + filename
            self.assertTrue(filecmp.cmp(file1,file2,shallow=False))

def checkCreateOutputFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def removeFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def klgtopng():
    
    f = open("2017-08-01.00.klg", "rb")

    # extract number of frames (32 bits)
    byte = f.read(4)
    a=map(ord,byte)
    numberofframes= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

    count=0

    # initialize images matrices
    depth = np.ones( (480,640),   dtype=np.uint16)
    rgb   = np.ones( (480,640,3), dtype=np.uint8)

    numberofframes = 10 #TOFIX: hack for testing

    while count<numberofframes:

        print count

        #reading timestamp
        byte = f.read(8)
        a=map(ord,byte)

        #reading depthsize
        byte = f.read(4)
        a=map(ord,byte)
        depthsize = a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

        #reading imagesize
        byte = f.read(4)
        a=map(ord,byte)
        imagesize = a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

        #extracting depth image
        byte = f.read(depthsize)
        dimage=zlib.decompress(byte)
        a=map(ord,dimage)
        for i in range(len(a)-1):
            depth[(i/1280)][(i%1280)/2]=a[i+1]*256+a[i]
        dname="klg2png_output/depth_aug/depth_aug"+str(count)+".png"
        cv2.imwrite(dname,depth)

        #extracting rgb image
        byte = f.read(imagesize)
        timage = np.fromstring(byte, dtype=np.uint8)
        rgb=cv2.imdecode(timage,1)
        cname="klg2png_output/rgb_aug/rgb_aug"+str(count)+".png"
        cv2.imwrite(cname,cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))

        count+=1

    f.close()

def extractFrames():

    f    = open("2017-08-01.00.klg", "rb")
    fout = open("outklg.klg", "wb")

    # extract number of frames (32 bits)
    byte = f.read(4)
    a=map(ord,byte)
    numberofframes= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

    # save to output file
    fout.write(byte);

    count=0

    # initialize images matrices
    depth = np.ones( (480,640),   dtype=np.uint16)
    rgb   = np.ones( (480,640,3), dtype=np.uint8)

    numberofframes = 10 #TOFIX: hack for testing

    while count<numberofframes:

        print count

        #reading timestamp
        byte = f.read(8)
        a=map(ord,byte)
        fout.write(byte)

        #reading depthsize
        byte = f.read(4)
        fout.write(byte)
        a=map(ord,byte)
        depthsize = a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

        #reading imagesize
        byte = f.read(4)
        fout.write(byte)
        a=map(ord,byte)
        imagesize = a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

        #extracting depth image
        byte = f.read(depthsize)
        fout.write(byte)

        #extracting rgb image
        byte = f.read(imagesize)
        fout.write(byte)

        count+=1

    f.close()
    

if __name__ == '__main__':
    removeFolder("klg2png_output");
    checkCreateOutputFolder("klg2png_output");
    checkCreateOutputFolder("klg2png_output/depth_aug/");
    checkCreateOutputFolder("klg2png_output/rgb_aug/");
    klgtopng()
    extractFrames()
    unittest.main()
