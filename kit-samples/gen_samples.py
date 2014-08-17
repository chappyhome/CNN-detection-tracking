# -*- coding: cp936-*-
__author__ = 'shuaiyi'
""" ����make_batch�����󣬲ɼ����������ͣ�
   1�������Ĵ�С���ã�64*64��
   2�������ı�ǩ���ã�Label��δ棬������δ����patch��
   3���������������ã���Ҫ����patch��ÿһ��������Σ�
"""
from util import extract
from util import kit
from util import utils
import shutil
import os
import sys
import numpy as np
import cv2

_size = 40

if os.path.exists('samples'):
    print 'Remove samples...'
    shutil.rmtree('samples')
    shutil.os.mkdir('samples')
    shutil.os.mkdir('samples/neg')
    shutil.os.mkdir('samples/pos')
else:
    print 'Make samples...'
    shutil.os.mkdir('samples')
    shutil.os.mkdir('samples/neg')
    shutil.os.mkdir('samples/pos')
  
samples_path = 'samples'  
training_data_path = 'Testing'

print 'Gen samples...'
datasets = kit.KIT(training_data_path)
datasets.extract_all()

for k,v in datasets.regions.items():
    region_name = k
    for frame_id, frame in v['frames'].items():
        img = cv2.imread(frame['img'],1)
        img = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)
        
        samples = extract.gen_neg_samples(region_name,frame_id,img,frame['cars'],200)
        utils.save_samples(samples_path + '/neg', samples)
        
        for car in frame['cars']:
            if max((int(car['w']),int(car['h']))) < 1.5*_size:
                samples = extract.get_sample(region_name, img, car, 5)
                utils.save_samples(samples_path + '/pos', samples)
            