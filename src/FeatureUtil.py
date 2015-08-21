__author__ = 'Tereka'

from sklearn import preprocessing
import pandas as pd
import numpy as np

from sklearn.feature_extraction import DictVectorizer

class FeatureVector(object):
    """
    This class is framework
    you should implement configuration.
    """
    def __init__(self):
        """
        you should set the feature name
        """
        self.name = ""
        self.list = None

    def convertFileToFeature(self):
        """
        you should implement convert csv to feature
        """

    def convertFlagToString(self,flag):
        if flag:
            return "t"
        else:
            return "f"

    def getVector(self,one_of_k=False,label_base=False,std=False,pca=False):
        train,labels,test = self.convertFileToFeature()
        self.std = std
        self.pca = pca
        self.one_of_k = one_of_k
        self.label_base = label_base

        if one_of_k:
            np_train,np_test = convertDataToNumpyArrayOneOfK(train,test,std=std,category_list=self.list)

        if label_base:
            np_train,np_test = convertDataToNumpyArrayBaseLabel(train,test,std=std,category_list=self.list)

        print np_train.shape,np_test.shape

        if pca:
            self.pca = pca
            """
            todo: to write the pca method
            """
        return np_train,labels,np_test

    def getFeatureName(self):
        suffix = ".pkl"
        word_list = []

        flag_list = [self.pca,self.std,self.one_of_k,self.label_base]
        flag_name_list = ["pca","std","one_of_k","label"]

        for flag,flag_name in zip(flag_list,flag_name_list):
            word = flag_name + "_" + self.convertFlagToString(flag)
            word_list.append(word)

        denominator = "_"
        feature_name = self.name
        for word in word_list:
            feature_name += denominator + word
        feature_name += suffix

        return feature_name

"""
if numpy.array is included number as column.
This program execute standardScaler Program.
"""
def scaleStandard(train,test):
    for i in xrange(train.shape[1]):
        if type(train[0,i]) != str:
            vector = np.hstack((train[:,i],test[:,i]))
            sds = preprocessing.StandardScaler()
            sds.fit(vector)
            train[:,i] = sds.transform(train[:,i])
            test[:,i] = sds.transform(test[:,i])
    return train,test

def scaleZeroToOne(train,test):
    for i in xrange(train.shape[1]):
        if type(train[0,i]) != str:
            vector = np.hstack((train[:,i],test[:,i]))
            minimize = np.min(vector)
            maximum = np.max(vector)

            train[:,i] = train[:,i]
            #test[:,i] = sds.transform(test[:,i])
    return train,test

"""
creation one of K expression
"""
def nparray_to_dictionary(data,category_list=None):
    dictionary_list = []
    for i in xrange(data.shape[0]):
        data_dictionary = {}
        for j in xrange(data.shape[1]):
            if category_list != None:
                if j in category_list:
                    data_dictionary[j] = str(data[i][j])
                else:
                    data_dictionary[j] = data[i][j]
            else:
                data_dictionary[j] = data[i][j]
        dictionary_list.append(data_dictionary)
    return dictionary_list

def data_to_labeled_encoder(train,test,category_list):
    for i in range(train.shape[1]):
        if i in category_list:
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(train[:, i]) + list(test[:, i]))
            train[:, i] = lbl.transform(train[:, i])
            test[:, i] = lbl.transform(test[:, i])
    return train,test

"""
convert data to numpy array
This numpy arrays are one of k expression
"""
def convertDataToNumpyArrayOneOfK(train,test,dataframe=False,std=True,category_list=None):
    if dataframe:
        train = np.array(train)
        test = np.array(test)
    if std:
        train,test = scaleStandard(train,test)

    data_train = nparray_to_dictionary(train,category_list)
    print data_train[0]
    data_test = nparray_to_dictionary(test,category_list)

    vec = DictVectorizer()
    vec.fit(data_train + data_test)
    print vec.vocabulary_
    train = vec.transform(data_train).toarray()
    test = vec.transform(data_test).toarray()

    return train.astype(float),test.astype(float)


def convertDataToNumpyArrayBaseLabel(train,test,dataframe=False,std=True,category_list=None):
    category_list= [0, 3, 5, 11, 12, 13, 14, 15, 16, 20, 22, 24, 26, 28, 30, 32, 34]
    if dataframe:
        train = np.array(train)
        test = np.array(test)
    if std:
        train,test = scaleStandard(train,test)

    train,test = data_to_labeled_encoder(train,test,category_list)
    return train.astype(float),test.astype(float)

if __name__ == '__main__':
    df = s1 = pd.Series([1.0,2.0,3.0,4.0,5.0], index=[0,1,2,3,4])
    s2 = pd.Series([10.0,20.0,70.0,40.0,50.0], index=[0,1,2,3,4])
    s3 = pd.Series([100,200,300,400,500], index=[0,1,2,3,4])
    s4 = pd.Series(["E","D","C","B","A"], index=[0,1,2,3,4])
    s5 = pd.Series(["XX","YY","ZZ","XX","YY"], index=[0,1,2,3,4])
    df = pd.concat([s1, s2,s3,s4,s5], axis=1)
    convertDataframeToNumpyArrayOneOfK(df,df)