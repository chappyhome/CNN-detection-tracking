# -*- coding: cp936 -*-
"""
Created on Mon May 11 14:44:33 2015

��Ҫ���Ƶ�ͼ���б�
1�����������ߴ������ϵ�ACC
2����ͬ���͵��������������ߴ��ָ��仯
3����Ϣ�ؼ���

@author: shuaiyi
"""
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import recall_score, precision_score, f1_score
from spm import SPMFeature
from PIL import Image
from entropy import entropy
import argparse
import pickle as pkl
import progressbar
import time, os
import logging
logging.getLogger().setLevel(logging.WARN)

from matplotlib import rcParams
# rcParams dict
rcParams['axes.labelsize'] = 10
rcParams['xtick.labelsize'] = 10
rcParams['ytick.labelsize'] = 10
rcParams['legend.fontsize'] = 10
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['figure.figsize'] = 7, 5

import matplotlib.pyplot as plt
import pylab
from scipy.stats import pearsonr

def figit(x, y, k):
    plt.figure()
    plt.plot(x[k], y[k], 'bo-')
    plt.title(k)
    plt.show()

"""Arguments"""
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "path to the dataset file (*.pkl)")
ap.add_argument("-c", "--clusters", type = int, default = 1000,
	help = "k-means clusters") 
ap.add_argument("-i", "--imgsize", type = int, default = 600,
	help = "image size") 
ap.add_argument("-n", "--iter", type = int, default = 10,
	help = "n iter") 
 
args = vars(ap.parse_args())
dataset = pkl.load(file(args["dataset"], 'rb'))

# ��������Ʊ���Ϊ����
le = LabelEncoder()
all_labels = dataset.keys()
le.fit(all_labels)

# TODO: ������Ϣ��,�ؿ���ͳһ�㣬�����CV���У�
if False:
    clusters = [1000]
    imgsize = [100,150,200,250,300,350,400,450,500,550,600]
    
    print "Compute Entropy..."
    all_ents = {}
    for k,v in dataset.items():
        print "Processing", k
        for c in clusters:
            for i in imgsize:
                tmp = 0
                key = "{0}_{1}".format(c, i)
                if not all_ents.has_key(key):
                    all_ents[key] = {}
                for item in v:
                    im = Image.open(item).convert('L')
                    if im.size[0] != i:
                        im = im.resize((i, i))
                    tmp += entropy(im)
                all_ents[key][k] = tmp/len(v)
    
    print "Computing ALL Avg."
    for c in clusters:
        for i in imgsize:
            tmp = 0
            key = "{0}_{1}".format(c, i)   
            for k,v in dataset.items():
                tmp += all_ents[key][k]
            all_ents[key]['all'] = tmp/19
    
    joblib.dump(value=all_ents, filename='RSDataset_entropy.pkl', compress=3)

if True:
    c=args['clusters']
    i=args['imgsize']
    all_results = {}
    key = "{0}_{1}".format(c, i)   
    fpath = "{0}_{1}_{2}.pkl".format(args['dataset'][0:-4], c, i)
    print "CV :", c, i
    all_ftrs = joblib.load(fpath, 'r')
    # �������ݼ�
    all_x=[]
    all_y=[]
    for k,v in all_ftrs.items():
        print "Loading features", k
        X = []
        Y = []
        for item in v:
            Y.append(k)
            X.append(item)
        Y = le.transform(Y)
        X = np.vstack(X)
        all_x.append(X)
        all_y.append(Y)
        
    all_x = np.vstack(all_x)
    all_y = np.hstack(all_y)

    # ͳ�ƴ�����һ�㣬�����ܲ���ƽ�����
    cv = StratifiedShuffleSplit(y=all_y, n_iter=args['iter'], test_size=0.4)
    
    precision=[]
    recall=[]
    f1=[]
    
    pbar = progressbar.ProgressBar(maxval=cv.n_iter).start()
    cnt = 0
    for train, test in cv:
        train_x, train_y, test_x, test_y = all_x[train], all_y[train], all_x[test], all_y[test]
        clf = SVC(C=1, kernel='linear', probability = True, random_state=42)
        clf.fit(train_x, train_y)
        pre_y = clf.predict(test_x)
        precision.append(precision_score(test_y, pre_y, average=None))
        recall.append(recall_score(test_y, pre_y, average=None))
        f1.append(f1_score(test_y, pre_y, average=None))
        pbar.update(cnt+1)
        cnt = cnt + 1
    
    pbar.finish()
    precision=np.vstack(precision)
    recall=np.vstack(recall)
    f1=np.vstack(f1)
    all_results = {"precision":precision,"recall":recall,"f1":f1}# ���˳��ܹؼ�

    # saving
    joblib.dump(value={"cv":all_results, "LabelEncoder":le}, filename='RSDataset_cv_%s.pkl'%key, compress=3)
    #print("Accuracy-%0.3f : %0.3f (+/- %0.3f)" % (c, scores.mean(), scores.std() * 2))
    
if False:
    # TODO: �������������
    clusters = [1000]
    imgsize = [100,150,200,250,300,350,400,450,500,550,600]
    
    print "Loading Entropy..."
    all_ents = joblib.load('RSDataset_entropy.pkl')
    print "Loading CV-DETAIL..."
    all_precision = {}
    all_recall = {}
    all_f1 = {}
    for c in clusters:
        for i in imgsize:
            key = "{0}_{1}".format(c, i)
            if not all_precision.has_key(key):
                all_precision[key] = {}
                all_recall[key] = {}
                all_f1[key] = {}
            fname = 'RSDataset_cv_%s.pkl'%key
            cv = joblib.load(fname)['cv']
            for i in range(19):
                print "Precision, Recall, F1 Loading..."
                k = str(le.inverse_transform([i])[0])
                all_precision[key][k] = cv['precision'][:,i]
                all_recall[key][k] = cv['recall'][:,i]
                all_f1[key][k] = cv['f1'][:,i]
    
    print "Loading CV-All..."
    all_scores = {}
    for c in clusters:
        for i in imgsize:
            key = "{0}_{1}".format(c, i)
            fname = 'RS_results/size_acc/RSDataset_%s.npy'%key
            score = np.load(fname)
            all_scores[key] = score
    
    #TODO: ����׼���ã��������ݷ���
    x_size = imgsize
    x_entropy_all = []
    y_scores_all = []
    x_entropy = {}
    y_scores_precision = {}
    y_scores_recall = {}
    y_scores_f1 = {}
    for s in x_size:
        key = "1000_{0}".format(s)
        #x_entropy_all.append(all_ents[key]['all'])
        y_scores_all.append(all_scores[key].mean())
        
        for k,v in all_ents[key].items():
            if not x_entropy.has_key(k):
                x_entropy[k] = []
            x_entropy[k].append(v)
            
        for k,v in all_precision[key].items():
            if not y_scores_precision.has_key(k):
                y_scores_precision[k] = []
            y_scores_precision[k].append(v.mean())
            
        for k,v in all_recall[key].items():
            if not y_scores_recall.has_key(k):
                y_scores_recall[k] = []
            y_scores_recall[k].append(v.mean())
            
        for k,v in all_f1[key].items():
            if not y_scores_f1.has_key(k):
                y_scores_f1[k] = []
            y_scores_f1[k].append(v.mean())
            
    x_entropy_all = x_entropy['all']
    x_entropy.pop('all')
        
    # �о����뾫��֮������������
    fit = pylab.polyfit(x_entropy_all,y_scores_all,1)
    fit_fn = pylab.poly1d(fit) 
    print "����������ྫ��֮������ϵ����", pearsonr(x_entropy_all, y_scores_all)
    
    # ������
    plt.figure()
    plt.subplot(131)
    plt.plot(x_size, y_scores_all,'bo-')
    plt.title("Size-Acc")
    
    plt.subplot(132)
    plt.plot(x_entropy_all, y_scores_all,'ro-', 
             x_entropy_all, fit_fn(x_entropy_all), '--k')
    plt.title("Entropy-Acc")
    
    plt.subplot(133)
    plt.plot(x_size, x_entropy_all,'go-')
    plt.title("Size-Entropy")    
    
    plt.show()
    
    # һ���򵥵��������ز��ǹؼ���������
    # ���ⲻͬ�������͵����ųߴ�϶��ǲ�ͬ�����Ǿ�������
    # ������Ͷ�㣬����һ���۲��ص�Ӱ��
    # ������Ͷ�㣬�о������뵥�����ķ������û�б�ȻӰ�죿����
    x_all_entropy = []
    y_all_precision = []
    for k in x_entropy.keys():
        x_all_entropy += x_entropy[k]
        y_all_precision += y_scores_precision[k]
    
    plt.figure()
    plt.scatter(x_all_entropy, y_all_precision)
    plt.title('Entropy-Precision')
    plt.show()
    
    # ��������
    # �������д󲿷��������ص���������������
    # �ǲ���10��̫�ٵ�ԭ��ͳ�����Ȳ���???
    for k in x_entropy.keys():
        figit(x_entropy, y_scores_f1, k)