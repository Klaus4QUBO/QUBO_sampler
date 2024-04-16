import sys
import numpy as np
import os
#++++++ reading model input in coo-like format from file ++++++++++++
input_data = os.getenv("INPUT_DATA_PATH")
DWave_in_matrix = np.genfromtxt(input_data)
print(DWave_in_matrix)
#++++++++++++++++++++++ model building ++++++++++++++++++++++++++++++
# DWave_in_matrix will be converted in COO-format for model building
print('\n')
# ... the Q-matrix to be solved has to be at least 1 column-vector
my_bqm = {(f'x{int(DWave_in_matrix[0,1])}', f'x{int(DWave_in_matrix[1,1])}'): DWave_in_matrix[2,1]}
if DWave_in_matrix[0,0] > 1 :  # reading out the number of column-vectors
    for k in range(1, (int(DWave_in_matrix[0,0]) + 1), 1) :
        # coo-format  ('key' : 'value')
        new_key = (f'x{int(DWave_in_matrix[0,k])}', f'x{int(DWave_in_matrix[1,k])}')
        # next value in sequence is assigned to new_key
        my_bqm[new_key] = int(DWave_in_matrix[2,k])
# >>>>>> Attention: 'int' to be deleted if 'values' are of real-type <<<<<<<<
else :
    print('Program aborted: The imported matrix does contain only 1 column of the Q-matrix!')
    sys.exit()
print(my_bqm)
print('\n')
#++++++++++++++++++++++ model to sampler ++++++++++++++++++++++++++++
# from dwave.system import DWaveSampler, EmbeddingComposite
# sampler = DWaveSampler()
# sampler_embedded = EmbeddingComposite(sampler)
# sampleset = sampler_embedded.sample_qubo(my_bqm, num_reads=5000)
# print(sampleset)
#+++++++++++ converting sampler output and writing to file +++++++++++
# string = str(sampleset)
# f=open("/Users/Klaus/Library/Mobile Documents/com~apple~CloudDocs/"
#       "Matlab Cloud/Datenaustausch/DWave_out.txt", "w")
# data = string
# f.write(data)
# f.close()