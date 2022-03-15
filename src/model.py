from __init__ import *

def main() -> any:
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
    h_bar, c, k_b, sigma = constants.hbar, constants.speed_of_light, constants.Boltzmann, constants.Stefan_Boltzmann
    c1 = h_bar*c**2/(4*np.pi**3)
    c2 = h_bar*c/k_b

    # TODO confirm normalization of bb spectrum.

    white_light_func = lambda k, T: 1/(sigma * T**4) * c1*k**3 * np.exp(-c2*k/T)/(-np.exp(-c2*k/T)+1)

    # Integrate out the temperature dependence

    after_interferometer_func = lambda k, OPD, T: white_light_func(k, T) * np.cos(OPD*k/2)**2 * 1/np.sqrt(2*np.pi*T_std**2) * np.exp(-(T-T_mean)**2/(2*T_std**2)) 
    T_vector = np.array(np.sort(np.random.normal(T_mean, T_std, int(1e9))))
    #output_function = lambda k_val, OPD_val: (sp.integrate.quad((lambda Temp: (after_interferometer_func(k=k_val, OPD=OPD_val, T=Temp))), 0.0, +np.inf, epsrel=1e-9))
    output_function = lambda k_val, OPD_val: sp.integrate.simpson(after_interferometer_func(k_val, OPD_val, T_vector), T_vector)

    print(output_function)

    # Test: TODO


    return output_function


