from __init__ import *

def main():
    """
    A routine for retruning the model that is expected from the setup, given perfect conditions
    in the form of a 2-valued input callable function (k, OPD) -> Intensity. This is to be fitted 
    to the simulated data in order to get deviations from the central pixel positions. The model 
    includes a temperature variation that is set up in the config file.
    """

    with open(os.path.join(DATA_DIR, 'config.json'), 'r') as infile:
        config = json.load(infile)


    T_mean = config['Temp_mean']
    T_std = config['Temp_std']
    h_bar, c, k_b = constants.hbar, constants.speed_of_light, constants.Boltzmann
    c1 = h_bar*c**2/(4*np.pi**3)
    c2 = h_bar*c/k_b

    white_light_func = lambda k, T: c1*k**3/(np.exp(c2*k/T)-1)
    white_light_norm = lambda T: (sp.integrate.quad((lambda k: (white_light_func(k, T))), 0.0, np.inf, epsrel=1e-12))
    white_light_normalized = lambda k, T: (white_light_func(k, T)/white_light_norm(T))
    after_interferometer_func = lambda k, OPD, T: white_light_normalized(k, T) * np.cos(OPD*k/2)**2 * 1/np.sqrt(2*np.pi*T_std**2) * np.exp(-(T-T_mean)**2/(2*T_std**2)) 

    output_function = lambda k_val, OPD_val: (sp.integrate.quad((lambda T: (after_interferometer_func(k=k_val, OPD=OPD_val, T))), 0.0, +np.inf, epsrel=1e-9))

    print(output_function)

    k_vec = 2*np.pi/np.linspace(3e-7, 7e-7 ,100, dtype=np.float64)
    OPD_vec = np.linspace(1.2e-3, 1.2005e-3, 100, dtype=np.float64)
    print(output_function(3e7, 1.2e-3))
    return output_function


