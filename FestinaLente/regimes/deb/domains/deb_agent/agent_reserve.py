


# Interaction ticks usable energy leftover

from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.agent_maintenance import SheepMaintenanceCosts



@dataclass
class InteractionBudget:
    """ useable somatic and maturity branch reserves """
    delta_t: float

    somatic_reserve: float
    per_tick_movement_reserve: float 
    maturation_reserve: float

    # methods inside dataclass? 

# delta_t new name
def get_interaction_reserve(maintenance_costs: SheepMaintenanceCosts, delta_t: int)-> InteractionBudget:

    somatic_day_reserve: float = maintenance_costs.soma_surplus_after_maintenance_J
    per_interaction: float = somatic_day_reserve/delta_t

    return InteractionBudget(
        delta_t=delta_t,
        somatic_reserve=somatic_day_reserve,
        per_tick_movement_reserve=per_interaction,
        maturation_reserve=maintenance_costs.maturity_surplus_after_maintenance_J
    )







    



