from __init__ import *

def main_step(indicator: int):
     """
     A routine for updating the estimates of the mean and its error on every pixel, summarizing the data from generator.
     """
     input_matrix = np.load(DATA, allow_pickle=True)['arr_0']
     output_matrix = np.load(DATA_1, allow_pickle=True)['arr_0']

     input_mean_matrix = input_matrix.mean(axis=0)
     output_mean_matrix = output_matrix[0]
     input_matrix_var = input_matrix.var(axis=0)
     output_matrix_var = output_matrix[1]

     mean_arr = (input_mean_matrix + indicator*output_mean_matrix)/(indicator+1)
     var_arr = (input_matrix_var/20 + (input_mean_matrix - mean_arr)**2/20 + indicator*(output_matrix_var*indicator + (output_mean_matrix - mean_arr)**2/20))/(indicator+1)**2


     #cv.imwrite("test_mean.png", 256*mean_arr/np.amax(mean_arr))
     #cv.imwrite("test_std.png", 256*var_arr/np.amax(var_arr))
        
     with open(os.path.join(DATA_DIR, "test.csv"), 'w') as testfile:
         writer = csv.writer(testfile)
         writer.writerows(var_arr)
    
     print(np.amax(var_arr))
     del input_matrix, output_matrix, input_mean_matrix, output_mean_matrix, input_matrix_var, output_matrix_var

     np.savez(DATA_1, [mean_arr, var_arr])
     os.remove(DATA)

     del mean_arr, var_arr

def main_init(indicator: int):
    """
    The first step of summarization
    """
    input_matrix = np.load(DATA, allow_pickle=True)

    mean_arr = input_matrix['arr_0'].mean(axis=0)
    var_arr = input_matrix['arr_0'].var(axis=0)/20
    np.savez(DATA_1, [mean_arr, var_arr])

    with open(os.path.join(DATA_DIR, "test.csv"), 'w') as testfile:
         writer = csv.writer(testfile)
         writer.writerows(var_arr)

    print(np.amax(var_arr))
    del input_matrix, mean_arr, var_arr
    os.remove(DATA)

def main(indicator: int):
    if(os.path.exists(DATA_1)):
        main_step(indicator)
    else:
        main_init(indicator)