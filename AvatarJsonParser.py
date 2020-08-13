#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:46:11 2020

@author: aaronatkinson
"""
import glob, pandas as pd

# glob in files
report_list = glob.glob('*.json')
#empty sample definition
sample = []
#empty dataframe to catch and concatenate samples
df3 = pd.DataFrame()
# loop through kraken2 reports
for report in report_list:
# get sample ID from filename drop file extension
sample_name = report.split('_')[-2]

# read in as pandas for specimen and diagnosis rows (rows 5 and 8)
grab = lambda x: x not in [19, 22, 23]
#pd.read_csv("data.csv", skiprows=pred, index_col=0, names=...)
sample = pd.read_csv(report, sep="\t", header=None, skiprows=grab)
sample = sample.transpose()

#pd.merge(sample, specimen.iloc[:, [1]], right_on=None)

#strip strings
sample[0] = sample[0].str.replace(r'"Specimen": "', '')
sample[0] = sample[0].str.replace(r'"', '')
sample[0] = sample[0].str.replace(r',', '')
sample[1] = sample[1].str.replace(r'"Diagnosis": "', '')
sample[1] = sample[1].str.replace(r'"', '')
sample[1] = sample[1].str.replace(r',', '')
sample[2] = sample[2].str.replace(r'"Prep": "', '')
sample[2] = sample[2].str.replace(r'"', '')
sample[2] = sample[2].str.replace(r',', '')
sample.columns = ['Specimen', 'Diagnosis', 'Tissue_Type']


# strip white space from name columns and redefine dictionary of diagnoses
sample.Specimen = sample.Specimen.str.strip()
sample.Diagnosis = sample.Diagnosis.str.replace('CG - ', '')
sample.Diagnosis = sample.Diagnosis.str.replace('Testis Cancer Biomarker', 'Testis')
sample.Diagnosis = sample.Diagnosis.str.replace('ColoCare', 'Colon')
sample.Diagnosis = sample.Diagnosis.str.replace(' Bronner', '')
sample.Diagnosis = sample.Diagnosis.str.strip()


#redefine sample "HCI_ID" column as sample_name, and re-order rows
sample.insert(0, 'HCI_ID', [sample_name], True)
#df3.sort_values(by=['HCI_ID'])

#Merge Patient_ID with Specimen Number
sample.insert(0, 'Patient', sample['HCI_ID'].str.cat(sample['Specimen'],sep="_"))
#reorder and drop unused columns
sample = sample.reindex(columns=['Patient', 'Diagnosis', 'Specimen', 'HCI_ID'])

#visualize and save to file
print(sample)
df3 = pd.concat([df3, sample], ignore_index=True)
df3.sort_values(by=['HCI_ID'])

df3.to_csv('AvatarJsonDiagnosis.tsv', sep='\t', index=False)
