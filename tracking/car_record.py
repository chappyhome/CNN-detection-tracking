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

def modulus(vec):
    return np.sqrt((vec*vec).sum())

class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        
    def dist(self, pt2):
        return math.sqrt((self.X - pt2.X)**2 + (self.Y - pt2.Y)**2)
        
    def vec(self):
        return np.array([self.X, self.Y])
        
    def __repr__(self):
        return '(%s,%s)'%(self.X, self.Y)

# Tracking Record
class Car:
    _id_ = 0
    def __init__(self, _loc, template = None, direction=None, oid=None, step_t = 0.4):
        """step_t������������֮��ļ��
        """
        self.hist_xy = list()
        self.hist_v = list()
        self.curr_v = 0
        self.curr_d = direction # �½���ʱ�򣬵�һ��direction��ģ�͹���ֵ

        self.m_id = Car._id_
        Car._id_ += 1 # ����ȫ�ֱ�����
        self.curr_xy = _loc
        self.step = step_t
        self.interval = 1
        self.is_new = True
        self.template = template
        self.dad = False
        self.oid = oid
    
    def update(self, t1_xy, direction):
        """���³�������Ҫ����Щ�ٶ�Ϊ�㣬���������ĳ����������⴦��
        """
        if self.curr_xy.dist(t1_xy) < 15: # ����ǳ����Ĵ�С
            self.curr_d = direction
        else:
            self.curr_d = direction
            # �����ٶ�
            self.curr_v = (self.curr_xy.vec() - t1_xy.vec())/(self.step*self.interval)
            #self.curr_v = self.curr_xy.dist(t1_xy)/self.step
        
        if not self.is_new:
            self.hist_v.append(self.curr_v)
        else:
            self.is_new = False
        
        self.hist_xy.append(self.curr_xy)
        self.curr_xy = t1_xy
     
    def dummy_update(self):
        if self.interval>2:
            self.dad = True
        else:
            self.interval += 1
     
    def cost(self, t1_all):
        # ��Ϊ4�����ͼ���ÿһ�����cost
        # ���self.history��Ϊ�գ�����type 1,2
        # ���self.historyΪ�գ�����type 3
        # �����ѡt1_allΪ�գ�����type 4
        pass
     
    def __repr__(self):
        if self.is_new:
            return "New Tracking: Initial Location (%s, %s)." % \
                (self.curr_xy.X, self.curr_xy.Y)
        else:
            return "Now : Location (%s, %s), Speed (%s m/s), Direction (%s)." % \
                (self.curr_xy.X, self.curr_xy.Y, modulus(self.curr_v) , self.curr_d)

# ��Ԫ����
class TestCar(unittest.TestCase):
    def setUp(self):
        self.m_car = Car(Point(0,0))

    def test_update(self):
        self.m_car.update(Point(30,40),45)
        self.m_car.update(Point(60,80),45)
        self.assertEqual(25, modulus(self.m_car.curr_v))
       
if __name__ == '__main__':
    #m_car = Car(0, Point(0,0))
    #m_car.update(Point(3,4),45)
    #m_car.update(Point(6,8),45)
    unittest.main()
    #print "Test!"
   

        
        