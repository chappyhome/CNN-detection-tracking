# -*- coding: cp936 -*-
"""
Created on Thu Mar 13 10:15:28 2014
���ڴ�prediction����У���ȡ�м�����
@author: shuaiyi
"""

import cPickle as pl
import numpy as np
import sys

result = pl.load(open(sys.argv[1],'rb'))
np.savetxt('labels.txt', result['labels'], delimiter=',')
np.savetxt('data.txt', result['data'], delimiter=',')