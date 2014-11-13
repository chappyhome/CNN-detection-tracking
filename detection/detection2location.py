# -*- coding: cp936 -*-
"""
/*code is far away from bug with the animal protecting
    *  ��������������
    *�����ߩ��������ߩ�
    *������������������ ��
    *������������������
    *�����ש������ס���
    *������������������
    *���������ߡ�������
    *������������������
    *������������������
    *�����������������ޱ���
    *��������������������BUG��
    *����������������������
    *���������������������ǩ�
    *������������������������
    *���������������ש�����
    *���������ϩϡ����ϩ�
    *���������ߩ������ߩ� 
    *������
    */

�����߼���

!!!�������⣺��ͬ�����ļ������Ҳ�ظ�����һ��
һ������ķ�������ͨ��������ָ�ټ�����ֵ���ˣ���ת��Ϊդ���ٽ�����̬ѧ������

���Ȱ�����Ӧ��С����һ����ֵ��������ʣ�µģ����к�������
1������ÿһ��region��ȡenv
2������wkt��תPolygon ȡ�ཻ����
3�����������ཻ������Ϊ�����

example:
ref:http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html
>>> from osgeo import ogr

>>> wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
>>> wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"

>>> poly1 = ogr.CreateGeometryFromWkt(wkt1)
>>> poly2 = ogr.CreateGeometryFromWkt(wkt2)

>>> intersection = poly1.Intersection(poly2)

>>> print intersection.ExportToWkt()

@author: shuaiyi
"""

import warnings
#�Զ��徯�洦�����������о������ε�
def customwarn(message, category, filename, lineno, file=None, line=None):
    pass

warnings.showwarning = customwarn

import os, sys, shutil
import progressbar # ������

try:
    from osgeo import ogr, osr
except:
    import ogr, osr
    
# ����ĳһ����Ŀ¼����������
prj_name = "MunichStreet03"
val_thre = 0.95
shp_list = []
for root, dirs, files in os.walk('segmentation/%s'%prj_name):
    for f in files:
        if f[-4:] == '.shp' and f[0:3] != 'WIN':
            shp_list.append(f)

driver = ogr.GetDriverByName('ESRI Shapefile')

if not os.path.exists('segmentation/%s/location'%prj_name):
    os.mkdir('segmentation/%s/location'%prj_name)
else:
    shutil.rmtree('segmentation/%s/location'%prj_name) # error 145 �ļ��зǿյ���
    shutil.os.mkdir('segmentation/%s/location'%prj_name)

for shp in shp_list:
    print "Processing segmentation/%s" % shp
    os.chdir("./segmentation/%s" % prj_name)
    dataSource = driver.Open(shp, 1) # ��Ҫ��д
    os.chdir(os.path.dirname(__file__))
    if dataSource is None: 
        print 'Could not open ' + fn
        sys.exit(1) #exit with an error code
    
    in_layer = dataSource.GetLayer(0)
    
    # ���ɼ�⵽��Polygon
    # ����ط�Ӧ��Ҳ��Ҫ�������ù���Ŀ¼ chdir    
    os.chdir('segmentation/%s/location'%prj_name)
    data_source = driver.CreateDataSource("WIN_%s" % shp)
    
    # create the spatial reference
    srs = osr.SpatialReference()
    
    # create the layer
    out_layer = data_source.CreateLayer("WIN_%s" % shp[:-4], srs, ogr.wkbPolygon)
    
    # Add the fields
    out_layer.CreateField(ogr.FieldDefn("value", ogr.OFTReal))
    
    # loop through the regions and get the detection window
    pbar = progressbar.ProgressBar(maxval=in_layer.GetFeatureCount()).start()
    
    cnt = 0
    feature = in_layer.GetNextFeature()
    extent = in_layer.GetExtent()
    height = abs(extent[2]-extent[3])
    while feature:
        # create the feature
        out_f = ogr.Feature(out_layer.GetLayerDefn())

        if feature.GetField("env") != None:
            # Set the attributes using the values from the delimited text file
            out_f.SetField("value", feature.GetField("value"))            
            cx, cy, w, h = [int(i) for i in feature.GetField("env").split(",")]
            
            """ !!! """
            # cy ��Ҫ����һ��
            cy = height - cy - h
            
            # create the WKT for the feature using Python string formatting
            wkt = "POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))" %  \
                  (cx, cy, cx+w, cy, cx+w, cy+h, cx, cy+h, cx, cy)
            poly = ogr.CreateGeometryFromWkt(wkt)
            
            out_f.SetGeometry(poly)
            # Create the feature in the layer (shapefile)
            out_layer.CreateFeature(out_f)
            #Destroy the feature to free resources
            out_f.Destroy()
        
        pbar.update(cnt+1)
        cnt = cnt + 1
        feature = in_layer.GetNextFeature()
            
    pbar.finish()


    # ��
    os.chdir(os.path.dirname(__file__))
    dataSource.Destroy()
    data_source.Destroy()
            