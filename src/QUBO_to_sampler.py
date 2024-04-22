import sys
import numpy as np
import os
import datetime
#
#++++++ reading model input in coo-like format from file ++++++++++++
#
input_link = os.getenv("INPUT_DATA_PATH")
DWave_in_matrix = np.genfromtxt(input_link)
#
#++++++++++++++++++++++ model building ++++++++++++++++++++++++++++++
# DWave_in_matrix will be adapted to COO-format for model building
# ++ 1 column-vector contains the number of succeeding column-vectors
#    condition: {number of succeeding column-vectors} > 1
# ++ succeeding column-vectors represent non-zero entries of the QUBO-matrix
#
my_bqm = {(f'x{int(DWave_in_matrix[0,1])}', f'x{int(DWave_in_matrix[1,1])}'): DWave_in_matrix[2,1]}
if DWave_in_matrix[0,0] > 1 :  # DWave_in_matrix[0,0] contains the number of column-vectors
    for k in range(1, (int(DWave_in_matrix[0,0]) + 1), 1) :
        # coo-format  ('key' : 'value')
        new_key = (f'x{int(DWave_in_matrix[0,k])}', f'x{int(DWave_in_matrix[1,k])}')
        # my_bqm is concatenated with new_key
        # next value in sequence is assigned to new_key
        my_bqm[new_key] = int(DWave_in_matrix[2,k])
# >>>>>> Attention: 'int' to be deleted if 'values' are intended to be of real-type <<<<<<<<
else :
    print('Program aborted: The imported matrix does contain only 1 column of the Q-matrix!')
    sys.exit()
# print(my_bqm)
# print('\n')
#
#++++++++++++ sampler call: bqm-model to sampler +++++++++++++++++++++
#
from dwave.system import DWaveSampler, EmbeddingComposite
sampler = DWaveSampler()
sampler_embedded = EmbeddingComposite(sampler)
sampleset = sampler_embedded.sample_qubo(my_bqm, num_reads=5000)
#
# ++++++++++++++ converting sampler timing information +++++++++++++++++
#
timing_info = sampleset.info["timing"]
timing_info_items = timing_info.items()
timing_info_list = list(timing_info_items)
timing_info_array = np.array(timing_info_list, dtype=object)
# print(timing_info_array)
#
# ++++++++++ implementing execution time +++++++++++++++++++++++++++++++
#
execute_time = datetime.datetime.now()
execute_time = execute_time.strftime('%a %d %b %Y, %I:%M%p')
#
# ++++++++++ joining output data and supplementary information +++++++++
#
DWave_out_matrix = ' '.join([str(sampleset), '\n', str(timing_info_array), '\n', str(execute_time)])
print('\n')
print(DWave_out_matrix)
#
# ++++++++++ writing composite output to file +++++++++++++++++++++++++++
#
output_link = os.getenv("OUTPUT_DATA_PATH")
f = open(output_link, "w")
f.write(DWave_out_matrix)
f.close()