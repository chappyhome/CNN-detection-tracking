# -*- coding: cp936 -*-
"""
Created on Fri Apr 24 09:11:50 2015

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.decomposition import SparseCoder, MiniBatchDictionaryLearning, RandomizedPCA #�׻��Լ��ֵ�
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte

from numpy.random import shuffle
import argparse
import logging
from sklearn.base import TransformerMixin,BaseEstimator

class Sparsecode(BaseEstimator, TransformerMixin):
    def __init__(self, patch_file=None, patch_num=10000, patch_size=(16, 16),\
                n_components=512,  alpha = 1, n_iter=1000, batch_size=100):
        self.patch_num = patch_num
        self.patch_size = patch_size
        self.patch_file = patch_file
        
        self.n_components = n_components
        self.alpha = alpha #sparsity controlling parameter
        self.n_iter = n_iter
        self.batch_size = batch_size

    
    def fit(self, X=None, y=None):
        if self.patch_file is None:
            num = self.patch_num // X.size
            data = []
            for item in X:
                img = imread(str(item[0]))
                img = img_as_ubyte(rgb2gray(img))
                #img = self.binary(img) # ��ֵ��
                tmp = extract_patches_2d(img, self.patch_size, max_patches = num,\
                                        random_state=np.random.RandomState())
                data.append(tmp)
            
            data = np.vstack(data)
            data = data.reshape(data.shape[0], -1)
            data = np.asarray(data, 'float32')
        else:
            data = np.load(self.patch_file,'r+') # load npy file, ע��ģʽ����Ϊ������Ҫ�޸�
        
        # whiten
        #print 'PCA Whiten...'
        #self.pca = RandomizedPCA(copy=True, whiten=True)
        #data = self.pca.fit_transform(data)
        
        # 0-1 scaling ��������preprocessingģ��ʵ��
        self.minmax = MinMaxScaler()
        data = self.minmax.fit_transform(data)
        #self.minmax.transform(data)
        
        #k-means
        self.kmeans = MiniBatchKMeans(n_clusters=self.n_components, init='k-means++', \
                                    max_iter=self.n_iter, batch_size=self.batch_size, verbose=1,\
                                    tol=0.0, max_no_improvement=100,\
                                    init_size=None, n_init=3, random_state=np.random.RandomState(0),\
                                    reassignment_ratio=0.0001)
        logging.info("Sparse coding : Phase 1 - Codebook learning (K-means).")
        self.kmeans.fit(data)
        
        logging.info("Sparse coding : Phase 2 - Define coding method (omp,lars...).")
        self.coder = SparseCoder(dictionary=self.kmeans.cluster_centers_, 
                                 transform_n_nonzero_coefs=256,
                                 transform_alpha=None, 
                                 transform_algorithm='omp')
        '''genertic
        self.dico = MiniBatchDictionaryLearning(n_components=self.n_components, \
                                           alpha=self.alpha, n_iter=self.n_iter, \
                                           batch_size =self.batch_size, verbose=True)
        self.dico.fit(data)
        '''
        return self
    
    def transform(self, X):
        #whiten
        #X_whiten = self.pca.transform(X)
        logging.info("Compute the sparse coding of X.")
        # 0-1 scaling ��������preprocessingģ��ʵ��
        X = np.require(X, dtype=np.float32)
        
        #TODO: �Ƿ�һ����Ҫ��fit������transform
        X = self.minmax.fit_transform(X)

        # MiniBatchDictionaryLearning
        # return self.dico.transform(X_whiten)
        
        # k-means
        # TODO: sparse coder method? problem...
        return self.coder.transform(X)
        
    
    def get_params(self, deep=True):
        return {"patch_num": self.patch_num,
                "patch_size":self.patch_size,
                "alpha":self.alpha,
                "n_components":self.n_components,
                "n_iter":self.n_iter,
                "batch_size":self.batch_size}
                
    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            self.__setattr__(parameter, value)
        return self
 

def show(components, patch_size):
    plt.figure(figsize=(4.2, 4))
    for i, comp in enumerate(components[:100]):
        plt.subplot(10, 10, i+1)
        plt.imshow(comp.reshape(patch_size),cmap=plt.cm.gray,
                   interpolation='none')
        plt.xticks(())
        plt.yticks(())
    plt.suptitle('100 components extracted by SC', fontsize=16)
    plt.subplots_adjust(0.08, 0.02, 0.92, 0.85, 0.08, 0.23)
    
    plt.show()
    
if __name__ == "__main__":
    """Arguments"""
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--patches", required = True,
                    help = "patch for patches saving")
    args = vars(ap.parse_args())
    
    patches = args["patches"]
    sc = Sparsecode(patches, n_iter=1000, batch_size=100)
    sc.fit()
    
    print 'Show...'
    show(sc.kmeans.cluster_centers_, (16,16))
    
    print 'Coding...'
    data = np.load(patches,'r+')[0:100]
    code = sc.transform(data)