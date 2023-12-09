import numpy as np
import pandas as pd
import os
import pbp_generation_function as pgf
import change_point_detection_function as cpdf
import plot_function as pf

# Step 1: generating PBP sequence
dirct = "input directory"
dirctout = "output directory" # specify positive / negative here
pgf.makedir(dirctout)

list_n = os.listdir(dirct)

for l in range(4,9):
    for h in range(4,9):
        pgf.pbpGen(dirct, dirctout, list_n, l, h)

#################################################

# Step 2: change point detection
dirct = "input directory" # pbp seq
outpath = "output directory" # change point seq
pgf.makedir(dirctout)
list_n = os.listdir(dirct)

K_list = [50,60,70,80,90,100,110,120]
cpdf.ChangePoint(dirct, outpath, list_n, label='positive_', K_list=K_list) # you can change 'label' for negative samples

#################################################

# Step 3a: computing accuracy
threshold_list = np.linspace(0.005,0.1,20)
dirct_n = 'negative pbp directory'
dirct_p = 'positive pbp directory'
dirctout_n = 'negative change point directory'
dirctout_p = 'negative change point dirdctory'
txtdirct = 'results .txt files directory'

pgf.makedir(txtdirct)

id_p = range(1, 14) # id of positive samples
id_n = range(1, 27) # id of negative samples

note = pd.read_excel("data.xlsx")
note = np.array(note[['total']])

cpdf.CompuRes(threshold_list, dirct_n, dirct_p, dirctout_n, dirctout_p, txtdirct, id_p, note, id_n)

# Step 3b: parameter selection (in R)

#################################################

# Step 4a: plotting
K = 120
threshold = 0.02

idx = id_p # change this for negative samples
outdirct = dirctout_p
plot_path = 'plot directory'
pgf.makedir(plot_path)

flag = 'positive' # change this for negative samples
 
pf.PlotSeq(K, threshold, dirct, idx, outdirct, note, plot_path, flag)

# Step 4b: performance evaluation
# See R plot / .txt files for sensitivity, specificity, error report rate and false alarm rate
num_false_candidate = 2 # This number and the next one are obtained from the plots in 4a.
num_positive_sample = 26

false_alarm_per_vedio = num_false_candidate / num_positive_sample # rate of false alarms per vedio (among positive samples)

