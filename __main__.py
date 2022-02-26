#!python3.9

from src import generator, summarize
from __init__ import *

print(DATA_DIR)

def cleanup():
    if(os.path.exists(DATA)):
        os.remove(DATA)
    if(os.path.exists(DATA_1)):
        os.remove(DATA_1)

def main():
    logging.basicConfig(filename="log.log", filemode='w', format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    indicator = 0
    while(True):
        if(not os.path.exists(DATA)):
            np.savez(DATA, generator.main())
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
            indicator = indicator + 1

            continue
        elif flag=='b':
            summarize.main(indicator)
            break
        else:
            return 1
    return 0

#def test():
 #   model.main()

if __name__ == "__main__":
    cleanup()
    main()
    #test()