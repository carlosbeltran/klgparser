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
    def __init__(self, testName, outputfolder, testfolder):
            super(TestKLGParser, self).__init__(testName) 
            self.outputfolder = outputfolder
            self.testfolder   = testfolder
    def testDepthOutput(self):
        _outputfolder = self.outputfolder
        _testfolder   = self.testfolder
        for indx in range(10):
            filename = "depth_aug" + str(indx) +".png"
            file1 = _outputfolder + filename
            file2 = _testfolder    + filename
            self.assertTrue(filecmp.cmp(file1,file2,shallow=False))
    def testRGBOutput(self):
        _outputfolder = self.outputfolder
        _testfolder   = self.testfolder
        for indx in range(10):
            filename = "rgb_aug" + str(indx) + ".png"
            file1 = _outputfolder + filename
            file2 = _testfolder   + filename
            self.assertTrue(filecmp.cmp(file1,file2,shallow=False))

def checkCreateOutputFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def removeFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def klgtopng(inputfile,firstframe,lastframe, outputfolder):
    
    f = open(inputfile, "rb")

    # extract number of frames (32 bits)
    byte = f.read(4)
    a=map(ord,byte)
    numberofframes= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

    count=0

    # initialize images matrices
    depth = np.ones( (480,640),   dtype=np.uint16)
    rgb   = np.ones( (480,640,3), dtype=np.uint8)

    #numberofframes = 10 #TOFIX: hack for testing

    while count < lastframe:

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
        if count >= firstframe and count < lastframe: 
            dimage=zlib.decompress(byte)
            a=map(ord,dimage)
            for i in range(len(a)-1):
                depth[(i/1280)][(i%1280)/2]=a[i+1]*256+a[i]
            dname= outputfolder + "depth_aug"+str(count)+".png"
            cv2.imwrite(dname,depth)

            #extracting rgb image
        byte = f.read(imagesize)
        if count >= firstframe and count < lastframe: 
            timage = np.fromstring(byte, dtype=np.uint8)
            rgb=cv2.imdecode(timage,1)
            cname= outputfolder + "rgb_aug"+str(count)+".png"
            cv2.imwrite(cname,cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))

        count+=1

    f.close()

def extractFrames(inputfile,outputfile,firstframe,lastframe):


    f    = open(inputfile, "rb")
    fout = open(outputfile, "wb")

    # extract number of frames (32 bits)
    byte = f.read(4)
    a=map(ord,byte)
    numberofframes= a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

    dstnumofframes = lastframe - firstframe;
    dstnumofframes = np.uint32(dstnumofframes);
    
    # save to output file
    fout.write(dstnumofframes);

    count=0

    # initialize images matrices
    depth = np.ones( (480,640),   dtype=np.uint16)
    rgb   = np.ones( (480,640,3), dtype=np.uint8)

    #numberofframes = 10 #TOFIX: hack for testing

    while count < lastframe:

        print count

        #reading timestamp
        byte = f.read(8)
        a=map(ord,byte)
        if count >= firstframe and count < lastframe: 
            fout.write(byte)

        #reading depthsize
        byte = f.read(4)
        if count >= firstframe and count < lastframe: 
            fout.write(byte)
        a=map(ord,byte)
        depthsize = a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

        #reading imagesize
        byte = f.read(4)
        if count >= firstframe and count < lastframe: 
            fout.write(byte)
        a=map(ord,byte)
        imagesize = a[3]*256*256*256+a[2]*256*256+a[1]*256+a[0]

        #extracting depth image
        byte = f.read(depthsize)
        if count >= firstframe and count < lastframe: 
            fout.write(byte)

        #extracting rgb image
        byte = f.read(imagesize)
        if count >= firstframe and count < lastframe: 
            fout.write(byte)

        count+=1

    f.close()
    

if __name__ == '__main__':

    dstimgfolder  = "klg2png_output/"
    imgtestfolder = "output_test/"

    # Preparing the environment
    removeFolder(dstimgfolder);
    checkCreateOutputFolder(dstimgfolder)

    # Actuating algorihtms
    extractFrames("2017-08-01.00.klg","outklg.klg",0,10)
    klgtopng("outklg.klg",0,10,dstimgfolder)

    # calling tests
    suite = unittest.TestSuite()
    suite.addTest(TestKLGParser('testDepthOutput', dstimgfolder, imgtestfolder))
    suite.addTest(TestKLGParser('testRGBOutput',   dstimgfolder, imgtestfolder))
    unittest.TextTestRunner(verbosity=2).run(suite)
