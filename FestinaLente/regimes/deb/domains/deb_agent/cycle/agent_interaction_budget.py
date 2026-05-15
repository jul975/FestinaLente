


# Interaction ticks usable energy leftover

from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.phases.maintenance import SheepMaintenanceCosts



@dataclass
class InteractionBudget:
    """ useable somatic and maturity branch reserves """
    delta_t: float

    somatic_reserve: float
    per_tick_movement_reserve: float 
    maturation_reserve: float

    max_locomotion_distance_m: float = 0.0
    max_distance_per_tick_m: float = 0.0


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




def compute_max_locomotion_distance_m(
        somatic_energy_J: float,
        c_transport_J_per_kg_m: float,
        body_mass_kg: float, 
        terrain_factor: float = 1.0) -> float:
    """ compute maximum locomotion distance in meters given available energy and cost per meter """
    if c_transport_J_per_kg_m <= 0:
        raise ValueError("Transport cost per kg per meter must be positive.")
    if somatic_energy_J <= 0:
        return 0.0  # No energy means no movement
    return somatic_energy_J / (c_transport_J_per_kg_m * body_mass_kg * terrain_factor)





    



