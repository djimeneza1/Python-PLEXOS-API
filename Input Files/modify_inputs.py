# -*- coding: utf-8 -*-
"""
Update PLEXOS attributes in an input dataset

Created on Sat Sep 09 19:19:57 2017

@author: Steven

TODO: P9 Failed
"""

import os, sys, clr
from shutil import copyfile

# load PLEXOS assemblies
#sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 9.0 API')
#clr.AddReference('PLEXOS_NET.Core')
#clr.AddReference('EEUTILITY')
#clr.AddReference('EnergyExemplar.PLEXOS.Utility')

plexospath='C:\Program Files\Energy Exemplar\PLEXOS 9.2 API'
sys.path.append(plexospath)
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import *
from EnergyExemplar.PLEXOS.Utility.Enums import *
from System import *

if os.path.exists('Input Files'): os.chdir('Input Files')

if os.path.exists('rts_PLEXOS.xml'):

    # delete the modified file if it already exists
    if os.path.exists('rts3.xml'):
        os.remove('rts3.xml')

    # copy the PLEXOS input file
    copyfile('rts_PLEXOS.xml', 'rts3.xml')
    
    # Create an object to store the input data
    db = DatabaseCore()
    db.Connection('rts3.xml')

    '''
    Int32 CopyObject(
    	String strName,
    	String strNewName,
    	ClassEnum nClassId
    	)
    '''
    db.CopyObject('Q1 DA','APIModel',ClassEnum.Model)
    db.CopyObject('Q1 DA','APIHorizon',ClassEnum.Horizon)
    
    '''
    Int32 RemoveMembership(
    	CollectionEnum nCollectionId,
    	String strParent,
    	String strChild
    	)
    '''
    db.RemoveMembership(CollectionEnum.ModelHorizon, 'Q1 DA', 'APIHorizon')
    db.RemoveMembership(CollectionEnum.ModelHorizon, 'APIModel', 'Q1 DA')
    
    '''
    Boolean UpdateAttribute(
    	ClassEnum nClassId,
    	String strObjectName,
    	Int32 nAttributeEnum,
    	Double dNewValue <--- always a Double... need to convert DateTime to Double
                         <--- using the ToOADate() method of the DateTime class
    	)
    '''    
    # a list of tuples... these tuples match the signature of UpdateAttribute and AddAttribute
    #   i.e., (ClassEnum, String, Int32, Double)
    attr = [(ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.DateFrom), DateTime(2024,1,1).ToOADate()),
            (ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.StepType), 4.0),
            (ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.StepCount), 1.0),
            (ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.ChronoDateFrom), DateTime(2024,2,15).ToOADate()),
            (ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.ChronoStepType), 2.0),
            (ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.ChronoAtaTime), 3.0),
            (ClassEnum.Horizon, 'APIHorizon', int(HorizonAttributeEnum.ChronoStepCount), 4.0)]

    # loop through the attributes to add/update    
    for param in attr:
        if not db.UpdateAttribute(*param):
            # if we cannot update it, add it
            db.AddAttribute(*param)

    # save the data set
    db.Close()
    