:ͨ���ָ���м�⣬����ΪͼƬ�ļ��м�shp�ļ��У���shp��ţ��б�Ҫ����һ�£�
rem segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results5 83 86
segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results10 83 86
segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results15 83 86
segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results20 83 86

:���ù�����䣬������Ҫ�ķָ���
rem filter_polys.py ./segmentation/MS04/results20/MOS83.shp value

:���ָ���ת��Ϊͼ�񣬷����һ��������̬ѧ�Ĵ���
rem poly2ras.py ./segmentation/MS04/results20/out_MOS83.shp
pause