set start=62
set end=99
set delta=95
set prj_name=MA
set img_pre=ON00

:ͨ���ָ���м�⣬����ΪͼƬ�ļ��м�shp�ļ��У���shp��ţ��б�Ҫ����һ�£�
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results5
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results10
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results15
REM segement_detection.py ./segmentation/MA01 ./segmentation/MA01/results20

REM segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results5
REM segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results10
REM segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results15
REM segement_detection.py ./segmentation/MS04 ./segmentation/MS04/results20

:���ù�����䣬������Ҫ�ķָ���
REM for /l %%i in (62,1,68) do filter_polys.py ./segmentation/MA01/results5/ON00%%i.shp 0.95

REM for /l %%i in (83,1,111) do filter_polys.py ./segmentation/MS04/results15/MOS%%i.shp 0.95
REM for /l %%i in (83,1,111) do filter_polys.py ./segmentation/MS04/results20/MOS%%i.shp 0.95
REM for /l %%i in (83,1,111) do filter_polys.py ./segmentation/MS04/results15/MOS%%i.shp 0.95
REM for /l %%i in (83,1,111) do filter_polys.py ./segmentation/MS04/results20/MOS%%i.shp 0.95

:���ָ���ת��Ϊͼ�񣬷����һ��������̬ѧ�Ĵ���
REM for /l %%i in (62,1,68) do poly2ras.py ./segmentation/MA01/results5/95out_ON00%%i.shp ./segmentation/MA01/results5/ON00%%i.shp

REM for /l %%i in (83,1,111) do poly2ras.py ./segmentation/MS04/results10/95out_MOS%%i.shp ./segmentation/MS04/results10/MOS%%i.shp
REM for /l %%i in (83,1,111) do poly2ras.py ./segmentation/MS04/results15/95out_MOS%%i.shp ./segmentation/MS04/results15/MOS%%i.shp
REM for /l %%i in (83,1,111) do poly2ras.py ./segmentation/MS04/results20/95out_MOS%%i.shp ./segmentation/MS04/results20/MOS%%i.shp

:���ָ�������λ�ã�����������
REM for /l %%i in (62,1,68) do ras2loc.py ./segmentation/MA01/ON00%%i.tif ./segmentation/MA01/results5/95out_ON00%%i.tif

for /l %%i in (85,1,111) do ras2loc.py ./segmentation/MS04/MOS%%i.tif ./segmentation/MS04/results5/95out_MOS%%i.tif
REM ./segmentation/MS04/results10/95out_MOS%%i.tif ./segmentation/MS04/results15/95out_MOS%%i.tif ./segmentation/MS04/results20/95out_MOS%%i.tif

REM ras2loc.py ./segmentation/MS04/MOS83.tif ./segmentation/MS04/results5/95out_MOS83.tif ./segmentation/MS04/results10/95out_MOS83.tif ./segmentation/MS04/results15/95out_MOS83.tif ./segmentation/MS04/results20/95out_MOS83.tif
pause