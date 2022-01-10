#!python3.9
from imports import *

import summarize
import generator

def cleanup():
    if(os.path.exists("data.npz")):
        os.remove("data.npz")
    if(os.path.exists("data_1.npz")):
        os.remove("data_1.npz")

def main():
    indicator = 0
    while(True):
        if(not os.path.exists("data.npz")):
            np.savez("data.npz", generator.main())
            print("Saved!")

        print("How should I proceed?")
        flag = ""
        try:
            flag = input()
        except EOFError:
            print("Error Detected")
            return 2

        if flag=='c':
            summarize.main(indicator)
            continue
        elif flag=='b':
            summarize.main(indicator)
            break
        else:
            return 1
        indicator = indicator + 1
    return 0

if __name__ == "__main__":
    cleanup()
    main()