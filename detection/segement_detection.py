# -*- coding: cp936 -*-
"""
Created on Fri Oct 17 19:51:20 2014
�����߼���
��ѡ������ֶα�ʶ�Ƿ�Ϊ������
1������ÿһ��region��ȡcenter xy
2����ȡoffset��
3�������ĵ�ȡȡ������ͼ��
4�����࣬Ϊ�ֶθ�ֵ

ע������⣺
��֤�����Ĳɼ�����ȷ��; xy�᲻Ҫ�����; ������ȷ

��߶ȷָ����ݣ�
������Ҫ����ķָ���ǿ����Ȳ�����ָ������£�����ȥ������Ҫ�����ݣ�
���ж�Ϊ����������ϲ���������ָ�

@author: shuaiyi
"""
import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning) 
#�Զ��徯�洦�����������о������ε�
def customwarn(message, category, filename, lineno, file=None, line=None):
    pass

warnings.showwarning = customwarn

import os, sys, math
import cv2 #ʹ��cv2��resize��ʵ��ͼ�������
import skimage.io as io #��дͼ��
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.util import img_as_ubyte
from sklearn.externals import joblib

import progressbar # ������
#import logging
#logging.getLogger()

try:
    from osgeo import ogr, gdal
except:
    import ogr, gdal

#from optparse import OptionParser
#
#parser = OptionParser()
#parser.add_option("-f", "--file", dest="image filename",
#                  help="source image file", metavar="FILE")
#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")
#
#(options, args) = parser.parse_args()


"""��������ֵ��γ�ȣ��Լ�դ�����Ϣ������Ӱ������
"""
def offset(ds, x, y):
    # get georeference info
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    # compute pixel offset
    xOffset = int((x - xOrigin) / pixelWidth)
    yOffset = int((y - yOrigin) / pixelHeight)
    return (xOffset, yOffset)

"""�ж�shp���Ƿ����ĳһ�ֶ�
"""
def is_exist(Layer,field_name):
    layerDefinition = Layer.GetLayerDefn()
    for i in range(layerDefinition.GetFieldCount()):
        if layerDefinition.GetFieldDefn(i).GetName() == field_name:
            return True
    return False

"""�õ�����feature���ڵ�raster��ΧӰ������
"""
def getRegion(r, f): # raster feature
    geo = f.GetGeometryRef()
    c_pt = geo.Centroid()
    cx, cy = offset(r, c_pt.GetX(), c_pt.GetY())
    
    l_x, r_x, d_y, u_y = geo.GetEnvelope() # ��¼��������Y���꣬�Լ�����x����
    env_w = r_x - l_x
    env_h = u_y - d_y
    max_len = math.sqrt(env_w**2 + env_h**2)
    env_area = env_w * env_h
    
    # sample size : 40
    w = h = 40
    in_size = 40

    #print cx , cy, w, h
    if cx - w/2 >= 0 and cx + w/2 <= r.RasterXSize \
    and cy - h/2 >= 0 and cy + h/2  <= r.RasterYSize:
        cx = cx - w/2
        cy = cy - h/2
    else:
        # ��Ե����
        if cx - w/2 < 0:
            cx = 0
        elif cx + w/2 > r.RasterXSize:
            cx = r.RasterXSize - w - 5 #
        else:
            cx = cx - w/2
            
        if cy - h/2 < 0:
            cy = 0
        elif cy + h/2 > r.RasterYSize:
            cy = r.RasterYSize - h - 5 #
        else:
            cy = cy - h/2
        
    img = r.ReadAsArray(cx ,cy , w, h)
    img = img.swapaxes(0,2).swapaxes(0,1)
    img = rgb2gray(img)
    img = resize(img, (in_size, in_size), mode='wrap')
    return img_as_ubyte(img.reshape((in_size, in_size,1))), (cx,cy,w,h), max_len, env_area
    #io.imsave("segementation/%s_%s_%s_%s.png" % \
    #         (lu_offset_x, lu_offset_y, w, h), img)
    #tmp = cv2.imread("segementation/%s_%s_%s_%s.png" % \
    #                (lu_offset_x, lu_offset_y, w, h))
    #return cv2.resize(tmp, (256,256), interpolation=cv2.INTER_LINEAR)
    #return resize(img, (256,256))

# ���� decaf �� classifier
from kitnet import DecafNet
net = DecafNet()

# ��ȡդ��ͼ��
gdal.AllRegister()

if len(sys.argv) != 5:
    print "Usage: segement_detection.py path_image_folder path_shp_folder start end"
    sys.exit()
else:
    image_folder = sys.argv[1]
    shp_folder = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

for i in range(start, end):
    g_raster = gdal.Open(image_folder+'/MOS%s.tif'%i, gdal.GA_ReadOnly) # ��ָ��ļ���Ӧ��ԭʼդ��
    
    print "Processing image " + image_folder+'/MOS%s.tif'%i
    # ��ȡ�ָ��� shp �ļ�
    driver = ogr.GetDriverByName('ESRI Shapefile')
    os.chdir(shp_folder)
    fn = "MOS%s.shp"%i
    dataSource = driver.Open(fn, 1) # ��Ҫ��д
    os.chdir(os.path.dirname(__file__))
    if dataSource is None: 
        print 'Could not open ' + fn
        sys.exit(1) #exit with an error code
    
    layer = dataSource.GetLayer(0)   
    
    # ����ֶ� slide 
    # ����Ѿ����ھͲ������
    if not is_exist(layer, "car"):
        fieldDefn = ogr.FieldDefn('car', ogr.OFTInteger)
        layer.CreateField(fieldDefn)
        
    if not is_exist(layer, 'value'):
        fieldDefn = ogr.FieldDefn('value', ogr.OFTReal)
        layer.CreateField(fieldDefn)
    
    if not is_exist(layer, 'env'):
        fieldDefn = ogr.FieldDefn('env', ogr.OFTString)
        layer.CreateField(fieldDefn)
    
    if not is_exist(layer, 'maxlen'):
        fieldDefn = ogr.FieldDefn('maxlen', ogr.OFTReal)
        layer.CreateField(fieldDefn)
        
    if not is_exist(layer, 'envarea'):
        fieldDefn = ogr.FieldDefn('envarea', ogr.OFTReal)
        layer.CreateField(fieldDefn)
    
    numFeatures = layer.GetFeatureCount()
    print 'Total region count:', numFeatures
    
    #test
    img = None
    TEST = False
    if TEST == True:
        feature = layer.GetNextFeature()
        img, env, maxlen, envarea = getRegion(g_raster, feature)
        scores = net.classify(img, False)
        is_car = net.top_k_prediction(scores, 2)
        if is_car[1][0] == 'car':
            print "Woh...a car..."
        raw_input("enter any character break:")
        break
    else:
        # loop through the regions and predict them
        pbar = progressbar.ProgressBar(maxval=numFeatures).start()
        
        cnt = 0
        feature = layer.GetNextFeature()
        while feature:
            # ��ȡ��Ӧ��ͼ������
            img, env, maxlen, envarea= getRegion(g_raster, feature)

            scores = net.classify(img, False)
            is_car = net.top_k_prediction(scores, 2)
            # print type(is_car[0][0])
            if is_car[1][0] == 'car':
                feature.SetField("car", 1)
                feature.SetField("value", float(is_car[0][0]))
            else:
                feature.SetField("car", 0)
                feature.SetField("value", float(is_car[0][1]))
            # ȫ�����
            
            feature.SetField("env", "%s,%s,%s,%s" % env)
            feature.SetField("maxlen", maxlen)
            feature.SetField("envarea", envarea)
            
            layer.SetFeature(feature) # ��һ���������ڱ����޸�
            pbar.update(cnt+1)
            cnt = cnt + 1
            feature = layer.GetNextFeature()
                
        pbar.finish()
    
    # close the data source
    dataSource.Destroy()
