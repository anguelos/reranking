#!/usr/bin/env python
import os.path
from commands import getoutput as go
import sys

def countDir(dName,ext='/*'):
    return len(go('echo '+dName+ext).split(' '))

def getHeatmaps(root):
    return [r.split('/')[-1] for r in go('echo '+root+'/*').split(' ') if r.split('/')[-1].startswith('hm')]

def getIoU(root):
    return [r.split('/')[-1] for r in go('echo '+root+'/*').split(' ') if r.split('/')[-1].startswith('iou_')]


def getConf(root):
    return [r.split('/')[-1] for r in go('echo '+root+'/*').split(' ') if r.split('/')[-1].startswith('conf_')]

def getInitials(root):
    if not os.path.isdir(root+'/input'):
        raise Exception('Not found')
    if not os.path.isdir(root+'/gt'):
        raise Exception('Not found')
    res=[root+'/input',root+'/gt']+getHeatmaps(root)
    if len(set([countDir(r,'/*') for r in res]))!=1:
        sys.err.write("Not All Files have the same file count\nAborting\n")
        sys.exit(1)


def generateProposals(root):
    print './src/hm2conf.py -threads=10 img2prop '+root+'/input/*jpg'
    print './src/hm2conf.py -threads=10 prop2conf '+root+'/proposals/*csv'


def generateHmConf(root):
    for hm in getHeatmaps(root):
        print './src/hm2conf.py -threads=10 hm2conf '+root+'/'+hm+'/*'

def generateThresholds(root,thresholdList):
    for threshold in thresholdList:
        for hm in getHeatmaps(root):
            print './src/hm2conf.py -thr='+str(threshold)+' -threads=10 hmThr '+root+'/'+hm+'/*'

def generateFusion(root,thresholdList):
    for threshold in thresholdList:
        for hm in getHeatmaps(root):
            print './src/hm2conf.py -thr='+str(threshold)+' -threads=10 hmThr '+root+'/'+hm+'/*'


def generateIoU(root):
    for conf in getConf(root):
        print './src/hm2conf.py -threads=10 conf2IoU '+root+'/'+conf+'/*'

# ./src/hm2conf.py  '-extraPlotDirs={".":"Weak Classifier","conf_hmCoco":"FCN COCO","conf_thr60_hmCoco":"FCN COCO > 0.60","conf_thr40_hmCoco":"FCN COCO > 0.4"}'  getCumRecall ./blabla/icdar_ch4_val/conf_proposals/img_* -maxProposalsIoU=100000 -care=1
if __name__=='__main__':
    if sys.argv[1]=='all':
        for dsName in sys.argv[2:]:
            generateProposals(dsName)
            generateHmConf(dsName)
            generateThresholds(dsName,[.1,.2,.3,.4,.5,.6,.7,.8])
            generateIoU(dsName)
        sys.exit(0)
    if sys.argv[1]=='conf':
        for dsName in sys.argv[2:]:
            generateHmConf(dsName)
            generateThresholds(dsName,[.1,.2,.3,.4,.5,.6,.7,.8])
        sys.exit(0)
    if sys.argv[1]=='iou':
        for dsName in sys.argv[2:]:
            generateIoU(dsName)
            #generateThresholds(dsName,[.1,.25])
        sys.exit(0)
    if sys.argv[1]=='clean':
        for dsName in sys.argv[2:]:
            dirs=[dsName+'/'+d for d in getIoU(dsName)]+[dsName+'/'+d for d in getConf(dsName)]
            print 'rm -Rf '+' '.join(dirs)
        sys.exit(0)