import os

import pandas as pd
import numpy as np

data = pd.read_csv("Données-élèves-2021/userStats.csv", sep=";")
print("load done")

directory = "Motivation"

file_list = []
file_name = []
for file in os.listdir(directory):
    file_list.append(os.path.relpath(file))

for n in file_list:
    split = n.split('pVals')
    if (len(split) > 1):
        file_name.append(split[0])

directory = ["Motivation"]

motiv_vector = []

# PART 1

for file in file_name:
    p_path = "Motivation" + "/" + file + "pVals.csv"
    val_path = "Motivation" + "/" + file + "PathCoefs.csv"
    pval = pd.read_csv(p_path, sep=';')
    val = pd.read_csv(val_path, sep=';')
    pval.drop(pval.columns[0], 1, inplace=True)
    pval = pval[pval <= 0.1]
    pval.fillna(False, inplace=True)
    pval = pval.astype('bool')
    val.drop(val.columns[0], 1, inplace=True)
    val = val[pval]
    val.fillna(0, inplace=True)
    motiv_vector.append([1 + val.iloc[0, :].sum(), 1 + val.iloc[1, :].sum(), 1 + val.iloc[2, :].sum()])

hexad_vector = []
for file in file_name:
    p_path = "Hexad" + "/" + file + "pVals.csv"
    val_path = "Hexad" + "/" + file + "PathCoefs.csv"
    pval = pd.read_csv(p_path, sep=';')
    val = pd.read_csv(val_path, sep=';')
    pval.drop(pval.columns[0], 1, inplace=True)
    pval = pval[pval <= 0.1]
    pval.fillna(False, inplace=True)
    pval = pval.astype('bool')
    val.drop(val.columns[0], 1, inplace=True)
    val = val[pval]
    val.fillna(0, inplace=True)
    temp_result_vector = []
    for column in val:
        temp_result_vector.append(1 + (val.loc[0, column] + val.loc[1, column] - val.loc[2, column]))
    hexad_vector.append(temp_result_vector)

student_data = pd.read_csv('Données-élèves-2021/userStats.csv', sep=';')
student = student_data.iloc[0, :]
student_hexad = student.iloc[10:16]
student_motiv = student.iloc[16:24]
student_motiv = [student_motiv.iloc[0:3].sum(), student_motiv.iloc[3:6].sum(), student_motiv.iloc[-1]]

result_motivation = []
result_hexad = []
for i in range(len(motiv_vector)):
    result_motivation.append(
        motiv_vector[i][0] * student_motiv[0] +
        motiv_vector[i][1] * student_motiv[1] -
        motiv_vector[i][2] * student_motiv[2]
    )

for i in range(len(file_name)):
    _sum = 0
    for j in range(len(hexad_vector)):
        _sum += student_hexad[i] * hexad_vector[i][j]
    result_hexad.append(_sum)

zipped_hexad = zip(result_hexad, file_name)
sorted_zipped_lists = sorted(zipped_hexad, reverse=True)
print("Selon les valeurs Hexad l'ordre d'importance est le suivant : ", sorted_zipped_lists)

zipped_motiv = zip(result_motivation, file_name)
sorted_zipped_lists = sorted(zipped_motiv, reverse=True)
print("Selon les valeurs de motivation  l'ordre d'importance est le suivant : ", sorted_zipped_lists)

# PART 2,3

norm_hexad = np.linalg.norm(result_hexad)
normal_hexad = result_hexad / norm_hexad

norm_motiv = np.linalg.norm(result_motivation)
normal_motiv = result_hexad / norm_motiv

repar_hexad = result_hexad / sum(result_hexad)
repar_motiv = result_motivation / sum(result_motivation)

mix_reco_vector = []

for i in range(len(normal_hexad)):
    mix_reco_vector.append((normal_hexad[i] * repar_hexad[i]) + (normal_motiv[i] * repar_motiv[i]))

zipped_mix = zip(mix_reco_vector, file_name)
sorted_zipped_lists = sorted(zipped_mix, reverse=True)
print("Selon l'Hexad et la motivation l'ordre d'importance est le suivant : ", sorted_zipped_lists)

# PART 2,4

delta_motiv = student_data[' micoVar'] + student_data[' miacVar'] + student_data[' mistVar'] + student_data[
    ' meidVar'] + student_data[' meinVar'] + student_data[' mereVar'] - student_data[' amotVar']
delta_motiv = delta_motiv > 0

print("nombre de cas ou l'élément a eu des effets positif : ", delta_motiv.sum())

print("nombre de cas ou l'élément a eu des effets négatif : ", len(delta_motiv) - delta_motiv.sum())

element_reco_pourc = []

for i in range(len(student_data)):
    student = student_data.iloc[i, :]
    student_hexad = student.iloc[10:16]
    student_motiv = student.iloc[16:24]
    student_motiv = [student_motiv.iloc[0:3].sum(), student_motiv.iloc[3:6].sum(), student_motiv.iloc[-1]]

    result_motivation = []
    result_hexad = []
    for i in range(len(motiv_vector)):
        result_motivation.append(
            motiv_vector[i][0] * student_motiv[0] +
            motiv_vector[i][1] * student_motiv[1] -
            motiv_vector[i][2] * student_motiv[2]
        )

    for i in range(len(file_name)):
        _sum = 0
        for j in range(len(hexad_vector)):
            _sum += student_hexad[i] * hexad_vector[i][j]
        result_hexad.append(_sum)

    norm_hexad = np.linalg.norm(result_hexad)
    # normal_hexad = result_hexad/norm_hexad
    normal_hexad = (result_hexad - min(result_hexad)) / (max(result_hexad) - min(result_hexad))

    norm_motiv = np.linalg.norm(result_motivation)
    # ↨normal_motiv = result_hexad/norm_motiv
    normal_motiv = (result_motivation - min(result_motivation)) / (max(result_motivation) - min(result_motivation))

    repar_hexad = normal_hexad / sum(normal_hexad)
    repar_motiv = normal_motiv / sum(normal_motiv)

    mix_reco_vector = []
    for i in range(len(normal_hexad)):
        mix_reco_vector.append((normal_hexad[i] * repar_hexad[i]) + (normal_motiv[i] * repar_motiv[i]))

    index = file_name.index(student[1])
    repartition = mix_reco_vector / sum(mix_reco_vector)
    element_reco_pourc.append(repartition[index])

element_reco_pourc = np.array(element_reco_pourc)
elem_pos_effect = element_reco_pourc[delta_motiv]
elem_neg_effect = element_reco_pourc[~delta_motiv]

from scipy.stats import ttest_ind

print(ttest_ind(elem_pos_effect, elem_neg_effect))


