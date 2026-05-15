

'''

state_t → energy ledger → state_t+1


E = total reserve energy, J
V = structural volume, cm³
L = structural length = V^(1/3), cm
[E] = reserve density = E / V, J/cm³
r = specific growth rate, 1/day => daily relative increase in structural volume
v / L = reserve turnover/conductance rate, 1/day



'''



from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.phases.flux import SheepFluxes
from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon

@dataclass(frozen=True)
class SheepMaintenanceCosts:
    """
    Tick-level maintenance accounting.

    Maintenance has priority over growth and maturation.
    """


    somatic_maintenance_due_J: float
    # Formula: C_S = [p_M] * V * dt

    somatic_maintenance_paid_J: float
    # Formula: min(B_S, C_S)

    somatic_deficit_J: float
    # Formula: max(C_S - B_S, 0)

    soma_surplus_after_maintenance_J: float
    # Formula: max(B_S - C_S, 0)
    


    maturity_maintenance_due_J: float
    # Formula: C_J = k_J * E_H * dt

    maturity_maintenance_paid_J: float
    # Formula: min(B_H, C_J)

    maturity_deficit_J: float
    # Formula: max(C_J - B_H, 0)

    maturity_surplus_after_maintenance_J: float
    # Formula: max(B_H - C_J, 0)





