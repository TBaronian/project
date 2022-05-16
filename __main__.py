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
    
    model_func = lambda x, params: 1e-7*(params['a'] + (1.0 + params['b'])*(x*1e7) + params['c']*(x*1e7)**2 + params['d']*(x*1e7)**3)
    def bb_func(**kwargs):
        observation = generator.main()
        print(observation.shape)
        model_mat = [[model.main(2*np.pi/lam_val, OPD_val) for lam_val in model_func(lambda_vector, kwargs)] for OPD_val in OPD_vector]
        print(np.array(model_mat).shape)

        objective = -np.sum(np.square(observation - model_mat))
        return objective

    """
    optimizer =  BayesianOptimization(
        f=bb_func,
        pbounds=pbounds
        )

    """
    #optimizer.maximize()

    value_mat = []
    value_vet = []
    params = {}
    for a in tqdm(np.linspace(pbounds['a'][0], pbounds['a'][1], 100)):
        value_vet = []
        for b in np.linspace(pbounds['b'][0], pbounds['b'][1], 100):
            params = params_0.copy()
            params['a'] = a
            params['b'] = b
            value_vet.append(bb_func(**params))
        value_mat.append(value_vet)

    plt.contourf(value_mat)
    plt.colorbar()
    np.savez(os.path.join(DATA_DIR, "power_data.npz"))
    plt.imsave(os.path.join(DATA_DIR, "third_pow.png"))
    
if __name__ == "__main__":
    test()
