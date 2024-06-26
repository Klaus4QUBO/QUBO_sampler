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
# DWave_in_matrix will be converted into COO-format for model building
# ++ 1st column-vector contains the number of succeeding column-vectors
# ++ succeeding column-vectors represent non-zero entries of the Q-matrix
# ++ of the QUBO-model
#
my_bqm = {(f'x{int(DWave_in_matrix[0,1])}', f'x{int(DWave_in_matrix[1,1])}'):
              float(DWave_in_matrix[2,1])}
# if DWave_in_matrix[0,0] > 1 :  # DWave_in_matrix[0,0] contains the number
                               # of column-vectors
for k in range(1, (int(DWave_in_matrix[0,0]) + 1), 1) :
    # coo-format  ('key' : 'value')
    new_key = (f'x{int(DWave_in_matrix[0,k])}', f'x{int(DWave_in_matrix[1,k])}')
    # my_bqm is concatenated with new_key
    # next value in sequence is assigned to new_key
    my_bqm[new_key] = float(DWave_in_matrix[2,k])
# >>>>>> Reminder: change 'float' to 'int' <<<<<<<<
# >>>>>> if 'values' are of integer type <<<<<<<<
#
# ++++++++++++ invoke sampler: bqm-model to sampler +++++++++++++++++++++
#
from dwave.system import DWaveSampler, EmbeddingComposite
sampler = DWaveSampler()
sampler_embedded = EmbeddingComposite(sampler)
sampleset = sampler_embedded.sample_qubo(my_bqm, num_reads=6000)
#
# ++++++++ Reading out and converting sampler timing information ++++++++
#
timing_info = sampleset.info["timing"]
timing_info_items = timing_info.items()
timing_info_list = list(timing_info_items)
timing_info_array = np.array(timing_info_list, dtype=object)
# print(timing_info_array)
#
# +++++++++++++++ reading out execution date +++++++++++++++
#
execute_time = datetime.datetime.now()
execute_time = execute_time.strftime('%a %d %b %Y, %I:%M%p')
#
# ++++++++++++ joining time and date information ++++++++++++
#
timing_data = ' '.join([str(timing_info_array), '\n', str(execute_time)])
print('\n')
print(timing_data)
#
# ++++++++++ writing timing and date information to file ++++++++++
#
output_link_2 = os.getenv("OUTPUT_DATA_PATH_TIMING")
f = open(output_link_2, "w")
f.write(timing_data)
f.close()
#
####################################################################
# The objective of the following section is to extract the 3 best
# solutions (lowest energy level) from sampler output data.
####################################################################
#
# +++++++++++++++++ Reading out 'sampleset' data ++++++++++++++++++
# +++++++++++++ to extract overall solver information +++++++++++++
#
print('\n')
# Converting 'sampleset' into string data
sample_out_all = str(sampleset)
sample_out_summary = sample_out_all[sample_out_all.find('[')+1 : len(sample_out_all)-1]
#
# ++++++++++++ reading out 'sampleset.data' data ++++++++++++
#
sample_out = str(sampleset.data) # (fields=['sample', 'energy'], sorted_by='energy'))
# print(sample_out)
#
# ++++++++ extracting binary solution variables from 'sampleset.data' data ++++++++
#
a_start = sample_out.find('([')
a_end = sample_out.find('...')
# determine and storing start and end value of each row
row_start = np.ones((3, 1), dtype=np.int16)
row_end = np.ones((3, 1), dtype=np.int16)
# ... out_detail will contain the extracted solution data
out_detail = ''
# ... cutting out binary solution data from first 3 rows
for k in range(0, 3):
    row_start[k] = sample_out.find('([', a_start + 2, a_end)
    row_end[k] = sample_out.find('),', row_start[k][0], a_end)
    row_end[k] = sample_out.rfind(',', row_start[k][0], row_end[k][0])
    out_detail = out_detail + sample_out[row_start[k][0]+1:row_end[k][0]] + '\n'
    a_start = row_end[k][0]
#
# ++++++++++++ joining solution data and overall solver information ++++++++++++
#
out_detail = out_detail + '\n' + sample_out_summary
print(out_detail)
#
# ++++++++++ writing solution data from 'sampleset.data' to file ++++++++++
#
output_link_3 = os.getenv("OUTPUT_DATA_PATH_RESULT")
f = open(output_link_3, "w")
f.write(out_detail)
f.close()
#
######################## +++ for test purposes +++ ########################
#
output_link_4 = os.getenv("OUTPUT_TEST_PATH")
f = open(output_link_4, "w")
f.write(sample_out)
f.close()