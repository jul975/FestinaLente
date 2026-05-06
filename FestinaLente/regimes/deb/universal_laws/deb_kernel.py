

'''

state_t → energy ledger → state_t+1


E = total reserve energy, J
V = structural volume, cm³
L = structural length = V^(1/3), cm
[E] = reserve density = E / V, J/cm³
r = specific growth rate, 1/day => daily relative increase in structural volume
v / L = reserve turnover/conductance rate, 1/day



'''



def K_deb(state_t, species_constants, derived_constants, tick_inputs):
    """ can move species constants and derivations out of the agent class """
    # → tick_budget
    # → state_t+1