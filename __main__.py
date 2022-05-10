#!python3.9

from src import generator, summarize, model
from __init__ import *

def cleanup():
    if(os.path.exists(DATA)):
        os.remove(DATA)
    if(os.path.exists(DATA_1)):
        os.remove(DATA_1)

def main():
    logging.basicConfig(filename="log.log", filemode='w', format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    indicator = 0

    def summarize_main():
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


def test():
    with open(os.path.join(DATA_DIR, "config.json"), 'r') as infile:
        config = json.load(infile)

    lambda_vector = np.linspace(config['lambda_min'], config['lambda_max'], config['lambda_N'])
    OPD_vector = np.flip(np.linspace(config['OPD_min'], config['OPD_max'], config['OPD_N']))
    
    params_0 = {'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0}
    pbounds = {k: (params_0[k]-0.001, params_0[k]+0.001) for k in params_0.keys()}
    
    model_func = lambda x, params: params['a'] + (1.0 + params['b'])*x + params['c']*x**2 + params['d']*x**3
    def bb_func(**kwargs):
        observation = generator.main()
        model_mat = [[model.main()(2*np.pi/lam_val, OPD_val) for lam_val in model_func(lambda_vector, kwargs)] for OPD_val in OPD_vector]

        objective = -np.sum(np.square(observation - model_mat))

    optimizer =  BayesianOptimization(
        f=bb_func,
        pbounds=pbounds
        )

    optimizer.maximize()
    

if __name__ == "__main__":
    test()