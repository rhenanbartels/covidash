# This is a custom model to used in place of Epigrass' built-in models. Custom
# models must always be on a file named CustomModel.py and contain at least 
# a function named Model. Both the File name and the function Names are case-sensitive,
# so be careful. Please refer to the manual for intructions on how to write your 
# own custom models.


##### Defining variable names to appear in the database
# Must be listed in the same order of variables they are returned by the model
vnames = ['Exposed', 'Infectious','Asymptomatic','Hospitalized', 'Susceptible']


def Model(inits, simstep, totpop, theta=0, npass=0, bi={}, bp={}, values=(), model=None):
    """
    This function implements the SEQIAHR model
    - inits = (E,I,S)
    - theta = infectious individuals from neighbor sites
    :param inits: Initial conditions
    :param simstep: Simulation step
    :param totpop: Total population on node
    :param theta: number of infectious arriving
    :param npass: total number of individual arriving
    :param bi: state variables (dict)
    :param bp: parameters (dict)
    :param values: Extra variables passed on nodes.csv
    :param model: reference to model instance
    :return:
    """
    # print(bi)
    ##### Get state variables' current values
    if simstep == 1:  # get initial values
        E, I, A, H, S = (bi[b'e'], bi[b'i'], bi[b'a'], bi[b'h'], bi[b's'])
    else:  # get last step value, in the order returned by this function
        E, I, A, H, S = inits

    ##### Defining N, the total population
    N = totpop

    ##### Getting values for the model parameters
    beta, alpha, chi, phi, delta, rho, q, p = (
        bp[b'beta'], bp[b'alpha'], bp[b'chi'], bp[b'phi'], bp[b'delta'], bp[b'rho'], bp[b'q'], bp[b'p'])

    ##### Defining a Vacination event (optional)
    if bp[b'vaccineNow']:
        S -= bp[b'vaccov'] * S

    ##### Modeling the number of new cases (incidence function)
    Lpos = beta * S * (I + A + (1 - rho) * H)  # Number of new cases

    ##### Epidemiological model (SIR)
    Epos = E + Lpos - alpha * E
    Ipos = I + (1 - p) * alpha * E - (phi + delta) * I
    Apos = A + p * alpha * E - delta * A
    Hpos = H + phi * I - delta * H
    Spos = S - Lpos
    Rpos = N - S + E + I + A + H

    # Number of infectious individuals commuting.
    migInf = Ipos + Apos

    return [Epos, Ipos, Apos, Hpos, Spos], Lpos, migInf
