import os
import numpy as np
import cv2 as cv
import csv

def main_step(indicator: int):
     input_matrix = np.load("data.npz", allow_pickle=True)
     output_matrix = np.load('data_1.npz', allow_pickle=True)

     mean_arr = (input_matrix['arr_0'].mean(axis=0) + output_matrix['arr_0'][0]*indicator)/(indicator+1)
     std_arr = np.sqrt(input_matrix['arr_0'].std(axis=0)**2/20 + output_matrix['arr_0'][1]**2*indicator**2)/np.sqrt(indicator+1)
     cv.imwrite("test_mean.png", 256*mean_arr/np.amax(mean_arr))
     cv.imwrite("test_std.png", 256*std_arr/np.amax(std_arr))
        
     with open("test.csv", 'w') as testfile:
         writer = csv.writer(testfile)
         writer.writerows(std_arr)
    
     print(np.amax(std_arr))
     del input_matrix

     np.savez('data_1.npz', [mean_arr, std_arr])
     os.remove("data.npz")

def main_init(indicator: int):
    input_matrix = np.load("data.npz", allow_pickle=True)

    mean_arr = input_matrix['arr_0'].mean(axis=0)
    std_arr = input_matrix['arr_0'].std(axis=0)/np.sqrt(20)
    np.savez('data_1.npz', [mean_arr, std_arr])

    with open("test.csv", 'w') as testfile:
         writer = csv.writer(testfile)
         writer.writerows(std_arr)

    print(np.amax(std_arr))
    del input_matrix
    os.remove("data.npz")

def main(indicator: int):
    if(os.path.exists("data_1.npz")):
        main_step(indicator)
    else:
        main_init(indicator)