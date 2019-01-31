#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 07:37:52 2019

@author: preston
"""
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from Acceleration import Acceleration #now you're the client

def userInput(option = 1):
    
    root = tk.Tk()
    root.withdraw()
    
    fs = input('What is the sampling frequency (Hz)? ')
    dic = {}
    moreSubjects = 'y'
    while moreSubjects.lower() == 'y':
        subjectName = input('What is the subject ID? ')
        dic[subjectName] = {}
        DA = input('Which is the dominant arm (L/R)? ')
        moreTrials = 'y'
        while moreTrials.lower() == 'y':
            trialName = input('What is the trial name? ')
            L = filedialog.askopenfile(title='Please select a left file', parent = root)
            R = filedialog.askopenfile(title='Please select a right file', parent = root)
            dic[subjectName][trialName] = Acceleration(L, R, fs, DA, subjectName)
            moreTrials = input('More trials for ' + subjectName + ' (y/n)? ')
        moreSubjects = input('More subjects (y/n)? ')
    return fs, dic
#    if option is 2:
#        more = 'y'
#        categories = input('What are the treatment groups (separate with a comma)? ')
#        allFiles = {}
#        categories = [x.strip().lower() for x in categories.split(',')]
#        for item in categories:
#            allFiles[item] = []
#        while (more is 'y' or more is 'Y'):
#            cat = input('What treatment group is this? ')
#            subjectName = input('What is the subject ID? ')
#            DA = input('Which is the dominant arm? (L/R)? ')
#            leftFile = filedialog.askopenfile(title='Please select a left file', parent = root)
#            rightFile = filedialog.askopenfile(title='Please select a right file', parent = root)
#            allFiles[cat.lower()].append(Acceleration(leftFile, rightFile, fs, DA, subjectName))
#            root.update()
#            more = input('more files (y/n)? ')
#    elif option is 1:
#        more = 'y'
#        allFiles = {'Accel':[], 'Label':[]}
#        while (more is 'y' or more is 'Y'):
#            name = input('What treatment group is this? ')
#            DA = input('Which is the dominant arm (L/R)? ')
#            leftFile = filedialog.askopenfile(title='Please select a left file', parent = root)
#            rightFile = filedialog.askopenfile(title='Please select a right file', parent = root)
#            allFiles['Accel'].append(Acceleration(leftFile, rightFile, fs, DA))
#            allFiles['Label'].append(name)
#            root.update()
#            more = input('more files? (y/n) ')

def plotHist(dic, option = 1):
    if option is 1: 
        plt.figure()
        for oneAccelObject, name in zip(dic['Accel'], dic['Label']):
            plt.plot(oneAccelObject.binAvg, oneAccelObject.counts, label = name + ', %.3f' % oneAccelObject.mass + '% dominant arm')      
        plt.ylabel('Probability (%)') 
        plt.xlabel("Jerk Ratio")
        plt.axvline(x = 0.5, ls = '--', label = '0.5 Bimanual', color = 'b')
        plt.legend(loc = 'upper right')
    elif option is 2:
        for cat, AccelList in dic.items():
            if len(AccelList) > 0:
                for Accel in AccelList:
                    plt.figure()
                    plt.plot(Accel.binAvg, Accel.counts)
                    plt.ylabel('Probability (%)') 
                    plt.xlabel("Jerk Ratio")
                    plt.axvline(x = 0.5, ls = '--', label = '0.5 Bimanual', color = 'b')
                    plt.title(Accel.subjectName + ', ' + cat)
        
    
plt.close('all')
fs, dic = userInput(option = 3)
#plotHist(allFiles, option = 2)

