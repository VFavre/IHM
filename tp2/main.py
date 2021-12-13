import os

import pandas as pd

data = pd.read_csv("Données-élèves-2021/userStats.csv", sep = ";")
print("load done")

directory = "Motivation"

file_list = []
file_name = []
for file in os.listdir(directory):
    file_list.append(os.path.relpath(file))

for n in file_list:
    split = n.split('pVals')
    if(len(split) > 1):
        file_name.append(split[0])

directory = ["Motivation"]

for d in directory:
    for file in file_name:
        p_path = d+ "/"+ file+ "pVals.csv"
        val_path = d+ "/"+ file+ "PathCoefs.csv"
        pval = pd.read_csv(p_path, sep = ';')
        val = pd.read_csv(val_path, sep = ';')
        pval.drop(pval.columns[0], 1, inplace = True)
        pval = pval[pval <= 0.1]
        pval.fillna(False, inplace = True)
        pval = pval.astype('bool')
        val.drop(pval.columns[0], 1, inplace = True)
        val = val[pval]
        # iterate over the colulns and row of the val dataframe and get the value of MI and ME that
        # are numerical in a list and the value of AM in another list

