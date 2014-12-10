# -*- coding: cp936 -*-

from __future__ import division
import unittest
import numpy as np
import math

'''
Created on Mon Dec 08 16:00:57 2014

@author: Administrator

һ��׷�ټ�¼����ʲô��
1 ��ʶID
2 ��ʷ���ݣ�λ�����ݣ���ǰ�ٶȣ�ƽ���ٶȣ���ǰ����
3 �Ƿ�Ϊ��׷��
4 �Ƿ��Ѿ�����

��Ԫ����
'''

class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        
    def dist(self, pt2):
        return math.sqrt((self.X - pt2.X)**2 + (self.Y - pt2.Y)**2)
        
    def __repr__(self):
        return '(%s,%s)'%(self.X, self.Y)

# Tracking Record
class Car:
    hist_xy = list()
    hist_v = list()
    curr_v = 0
    curr_d = None
    curr_xy = None
    m_id = None
    def __init__(self, _id, _loc, step_t = 2.0):
        self.m_id = _id
        self.curr_xy = _loc
        self.step = step_t
        self.is_new = True
    
    def update(self, t1_xy, direction):
        self.curr_d = direction
        # �����ٶ�
        self.curr_v = self.curr_xy.dist(t1_xy)/self.step
        if not self.is_new:
            self.hist_v.append(self.curr_v)
        else:
            self.is_new = False
        
        self.hist_xy.append(self.curr_xy)
        self.curr_xy = t1_xy
     
    def cost(self, t1_all):
        # ��Ϊ4�����ͼ���ÿһ�����cost
        # ���self.history��Ϊ�գ�����type 1,2
        # ���self.historyΪ�գ�����type 3
        # �����ѡt1_allΪ�գ�����type 4
        pass
     
    def __repr__(self):
        return "Now : Location (%s, %s), Speed (%s m/s), Direction (%s)." % \
            (self.curr_xy.X, self.curr_xy.Y, self.curr_v, self.curr_d)

# ��Ԫ����
class TestCar(unittest.TestCase):
    def setUp(self):
        self.m_car = Car(0, Point(0,0))

    def test_update(self):
        self.m_car.update(Point(3,4),45)
        self.m_car.update(Point(6,8),45)
        self.assertEqual(2.5, self.m_car.curr_v)
       
if __name__ == '__main__':
    #m_car = Car(0, Point(0,0))
    #m_car.update(Point(3,4),45)
    #m_car.update(Point(6,8),45)
    unittest.main()
    #print "Test!"
   

        
        