#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# This file is part of Kuaa.
#
# Kuaa is a framework for the automation of machine learning experiments.
#
# It provides a workflow-based standardized environment for easy evaluation of
# feature descriptors, normalization techniques, classifiers and fusion
# approaches.
#
# Techniques of each kind can be easily plugged into the framework as they can
# be implemented as plugins, with standardized inputs and outputs.
# The framework also provides a recommendation module in order to help
# inexperienced researchers in choosing adequate or alternative techniques for
# experiments.
#
# Copyright (C) 2016 under the GNU General Public License Version 3.
#
# This framework was developed during the research collaboration of Institute
# of Computing (University of Campinas, Brazil) and Samsung Eletrônica da
# Amazônia Ltda. entitled "Pattern recognition and classification by feature
# engineering, *-fusion, open-set recognition, and meta-recognition", which was
# sponsored by Samsung.
#
# This framework is provided "as is" without any guarantees or warranty. The
# authors make no warranties, express of implied, that they are free of error,
# or they will meet your requirements for any particular application.
#
# The framework was developed to be used for educational and research purposes.
# It is expressly prohibited to use for any commercial purposes.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

#Python imports
from __future__ import division #import to change the operation '/' to return
                                #a float
import os
from numpy import array
from sklearn.preprocessing import MinMaxScaler

#CONSTANTS
POS_CLASSES = 0
POS_FV = 1
INDEX_ZERO = 0

def normalize(img_path, images, images_set, pos_train_test, parameters, method,
        train_param):
    """
    Function that performs the normalization of a feature vector.
    
    Normalize the feature vector in the interval defined by the user.
    """
    
    print "Normalizer: MIN MAX"
    
    #Get the list of classes and the feature vector of the img_path
    img_classes = images[img_path][POS_CLASSES]
    try:
        img_fv = images[img_path][POS_FV][pos_train_test]
    except:
        img_fv = images[img_path][POS_FV][0]
    
    print "\tFeature vector of image", img_path, \
          "being normalized by process", os.getpid()
    
    # Performs the normalization ---------------------------------------------
    #Get values of min and max from the parameters
    new_min = parameters['Min']
    new_max = parameters['Max']
    
    #If the execution is of the train step, get the train_param, if it exists
    if 'Scale' not in train_param:
        scale = MinMaxScaler([new_min, new_max])
        scale = train_min_max(images, images_set, pos_train_test, scale)
        train_param['Scale'] = scale
    else:
        print "\t\tGet Scale"
        scale = train_param['Scale']
    
    fv_norm = scale.transform(array(img_fv)).tolist()
    #-------------------------------------------------------------------------
    
    return img_path, len(img_classes), img_classes, fv_norm, train_param

def train_min_max(images, images_set, pos_train_test, scale):
    """
    Fit the training features in the scale.
    """
    
    #Gather all training feature vectors
    training = []
    for img in images_set:
        try:
            training.append(images[img][POS_FV][pos_train_test])
        except:
            training.append(images[img][POS_FV][INDEX_ZERO])
    training = array(training)
    
    #Performs the scale fit
    scale = scale.fit(training)
    
    return scale
