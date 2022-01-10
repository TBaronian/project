import numpy as np
import csv

data_matrix = np.load("data_1.npz", allow_pickle=True)
with open('test.csv', 'w') as writefile:
    writer = csv.writer(writefile)
    writer.writerows(data_matrix['arr_0'][1])

writefile.close()