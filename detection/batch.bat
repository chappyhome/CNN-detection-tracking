:ͨ���ָ���м�⣬����ΪͼƬ�ļ��м�shp�ļ��У���shp��ţ��б�Ҫ����һ�£�
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results5
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results10
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results15
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results20

:���ù�����䣬������Ҫ�ķָ���
REM for /l %%i in (62,1,68) do filter_polys.py ./segmentation/MA01/results5/ON00%%i.shp 0.95

:���ָ���ת��Ϊͼ�񣬷����һ��������̬ѧ�Ĵ���
REM for /l %%i in (62,1,68) do poly2ras.py ./segmentation/MA01/results5/95out_ON00%%i.shp ./segmentation/MA01/results5/ON00%%i.shp

:���ָ�������λ�ã�����������
for /l %%i in (62,1,68) do ras2loc.py ./segmentation/MA01/ON00%%i.tif ./segmentation/MA01/results5/95out_ON00%%i.tif
pause