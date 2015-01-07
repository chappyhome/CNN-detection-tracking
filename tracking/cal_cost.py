# -*- coding: cp936 -*-
"""
Created on Mon Dec 08 14:14:32 2014

@author: Administrator
"""

import numpy as np
import os, sys, math

from car_record import Point, Car, modulus
from skimage.feature import match_template, peak_local_max
from skimage.color import rgb2gray

# �����뾶
# ����ȷ����ѡƥ��������뾶
search_r = 60 # ��λΪpixels

def unit_vector(vector):
    """ Returns the unit vector of the vector.  
        ����һ�������ĵ�λ��������ģΪ1.
    """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
        ������������֮��ļн�
            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle


#==============================================================================
# def gauss2D(shape=(5,5),sigma=0.5):
#     """2D gaussian mask ����һ��2D��˹ģ�壺��
#         should give the same result as MATLAB's
#         fspecial('gaussian',[shape],[sigma])
#     """
#     m,n = [(ss-1.)/2. for ss in shape]
#     y,x = np.ogrid[-m:m+1,-n:n+1]
#     h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
#     h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
#     sumh = h.sum()
#     if sumh != 0:
#         h /= sumh
#     return h
# 
# def hist_xy(src, pt_list, k_size=5, d_num=20, a_num=20):
#     """����������ֱ��ͼ����
#         # ���룺bin_num��0-r��
#         # �Ƕȣ�bin_num��0-2*pi
#         # ������x��(1,0)�ļн�    
#     """
# 
#     k = gauss2D((k_size, k_size)) 
#     border = int(k_size/2)
#     d_nbin = [(math.ceil(search_r/d_num)*i, math.ceil(search_r/d_num)*(i+1)) for i in range(d_num+1)]
#     a_nbin = [(math.ceil(2*np.pi/a_num)*i, math.ceil(2*np.pi/a_num)*(i+1)) for i in range(a_num+1)]
#     result = np.zeros((len(d_nbin)+2*border, len(a_nbin)+2*border))
#     for pt in pt_list:
#         v = pt.vec() - src.vec()
#         dist = modulus(v)
#         if dist <= r:
#             tmp =  np.arctan2(v[1], v[0])
#             angle =  -tmp if tmp < 0 else 2*np.pi+tmp
#             idx_d = int(tmp/math.ceil(2*np.pi/a_num)) + border
#             idx_a = int(tmp/math.ceil(search_r/d_num))+ border
#             result[(idx_d-border):(idx_d+border+1), (idx_a-border):(idx_a+border+1)] += k
#     return result[border:-border,border:-border]
#     
#==============================================================================
def c_c(car_t, pt_t1):
    """����������Լ��Ȩ�أ���Ҫ�����ڿ�ʼ֡��ƥ��;
    """
    pass

def c_match(car_t, pt_t1, pt_img):
    """����NCC��һ�»����ϵ��������ģ��ƥ�䣬��������֮�䵽���ж��񣡣���
    ���������ɫ��Ϣ�᲻������׼ȷ�ȣ�
    """
    if car_t.template == None or pt_img == None:
        return 0, None
    temp = rgb2gray(car_t.template)
    image = rgb2gray(pt_img)
    
    result = match_template(image, temp)
    ij = np.unravel_index(np.argmax(result), result.shape)
    y, x = ij[::-1]
    h, w = result.shape
    center = Point(w/2, h/2)
    detect = Point(x, y)
    return (1-center.dist(detect)/(math.sqrt(2)*w/2)), result #�����ƥ��Ӱ���Լ�ģ��Ӱ����������

def find_pts(car_t, kdt):
    # kdt = KDTree(X, leaf_size=30, metric='euclidean')
    idx = kdt.query(car_t.curr_xy.vec(), k=10, return_distance=True)
    # ������ֵ�� search��r
    return idx[1][idx[0]<search_r]

def c_p(car_t, pt_t1):
    """ ���㵱ǰ����Ԥ�ڽ����Ŀ���֮��CpȨ��(����仯���µ�Ȩ�ر仯)
          ���car_t����track����Ҫ��д
    """
    #x_t_k = car_t.curr_xy.vec()
    #v_t_k = car_t.curr_v
    #x_t_1 = pt_t1.vec()
    #k+1 = car_t.intervel
    if False: #not car_t.is_new:
        r_hat = modulus(car_t.curr_xy.vec() + car_t.interval * car_t.curr_v - pt_t1.vec())
        return 1 - r_hat / search_r
    else:
        return 1 - car_t.curr_xy.dist(pt_t1)/(search_r) #/car_t.interval

def c_v(car_t, pt_t1):
    """ ���㵱ǰ������Ŀ���֮��CvȨ��(�Ƕȱ仯���µ�Ȩ�ر仯)
        ���car_t����track����Ҫ��д
    """
    if False: #not car_t.is_new:
        v_t = car_t.curr_v
        v_t1 = (car_t.curr_xy.vec() - pt_t1.vec())/(car_t.step*car_t.interval)
        dot = np.dot(v_t, v_t1)
        t_modulus = modulus(v_t)
        t1_modulus = modulus(v_t1)
        cos_angle = dot/(t_modulus*t1_modulus) # cosinus of angle between x and y
        return 0.5 + 0.5*cos_angle
    else:
        D = 360 - car_t.curr_d
        #print D, np.cos(np.radians(D)), np.sin(np.radians(D))
        v_t = unit_vector(Point(np.cos(np.radians(D)), np.sin(np.radians(D))).vec())
        v_t1 = unit_vector(car_t.curr_xy.vec() - pt_t1.vec())
        cos_angle = np.dot(v_t, v_t1) # ���ǰ��㲻���ᵼ��nanֵ
        if np.isnan(cos_angle):
            cos_angle = 1
        # print cos_angle, v_t, v_t1
        return 0.5 + 0.5*abs(cos_angle) #������������һ�¾��У���ʼ��ʱ����������

def cost(car_t, pt_t1, pt_img):
    cost1, result= c_match(car_t, pt_t1, pt_img) # ģ��ƥ��
    cost2 = c_v(car_t, pt_t1) # �Ƕ�
    cost3 = c_p(car_t, pt_t1) # ����
    
    # ����cost1 2 3 ֮��ı���
    if cost2 > 0.5 and cost3 > 0: # �Ƕ����ز����ϣ����迼��
        alpha = 0.5
        beta = 0.2
        return (alpha*cost1+beta*cost2+(1-alpha-beta)*cost3), cost1, cost2, cost3
    else:
        return 2, cost1, cost2, cost3