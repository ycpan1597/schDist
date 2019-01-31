import numpy as np
import math
import pandas as pd
from scipy import signal


class Acceleration:
    def __init__(self, leftFile, rightFile, fs, DA, subjectName):
        self.leftAccel, self.leftJerk, self.leftJerkMag = self.read(leftFile, int(fs))
        self.rightAccel, self.rightJerk, self.rightJerkMag  = self.read(rightFile, int(fs))
        self.JR, self.counts, self.binAvg, self.mass = self.jerkRatio(DA, int(fs))
        self.subjectName = subjectName
    # computes the magnitude of a list of 3D vectors
    def matMag(self, mat): 
        mag = []
        for row in mat:
            mag.append(math.sqrt(row[0]**2 + row[1]**2+ row[2]**2))
        return mag
    
    # reads and computes acceleration and jerk values
    def read(self, file, fs):
        # reads in acceleration
        accel = []
        df = pd.read_csv(file, header = 0, usecols = ['X', 'Y', 'Z'])
        accel.append(df.iloc[0:].values)
        accel = accel[0]
        
        # finds jerk
        jerk = []
        for i in range(len(accel) - 1):
            jerk.append(np.multiply(np.subtract(accel[i + 1], accel[i]), fs).tolist())
        return accel, jerk, self.matMag(jerk)
    
    # calculates jerk ratio and mass below JR = 0.5
    def jerkRatio(self, DA, fs, cutoff = 2.5,):
        def findMass(counts, binEdges, threshold = 0.5):
            # threshold should be between 0 and 1
            diff = binEdges[1] - binEdges[0]
            mass = 0
            for item in counts:
                i = 0
                while binEdges[i] < threshold: 
                    mass += item * diff
                    i += 1
            return mass
        
        def butterworthFilt(data, cutoff):
            filteredData =[]
            # user input
            order = 4
            fsampling = fs
            
            nyquist = fsampling/2 * 2 * np.pi # in rad/s
            cutoff = cutoff * 2 * np.pi # in rad/s
            b, a = signal.butter(order, cutoff/nyquist, 'lowpass')
            filteredData = signal.filtfilt(b, a, data)
            return filteredData
        
        
        L = self.leftJerkMag
        R = self.rightJerkMag
        
        # computes jerk ratio
        if DA == 'R' or DA == 'r':
            N = L # left; N for non-dominant
            D = R # right; D for dominant
        else:
            N = R
            D = L
        JR = np.divide(N, np.add(N, D))
        
        histBins = np.linspace(0.1, 0.9, 200) 
        counts = np.histogram(JR, histBins, density = True)[0] # extracts only the counts
        binAvg = 0.5*(histBins[1:] + histBins[:-1])
        
        # filters the counts
        if cutoff != 0:
            counts = butterworthFilt(counts, cutoff)
        mass = findMass(counts, binAvg)
            
        return JR, counts, binAvg, mass



    