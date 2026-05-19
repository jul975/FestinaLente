
from dataclasses import dataclass
from turtle import distance


from FestinaLente.core.fluxes.agent_flux import AgentFluxes

@dataclass
class AgentDayLedger:
    """ 
    Created by DAY_OPEN tick, 
    updated during interaction ticks, 
    and used in DAY_CLOSE tick to apply growth, maturity, reproduction, and death.
    """
    agent_id: int
    biological_day: int

    mobilized_J: float
    soma_after_maintenance_J: float
    maturity_after_maintenance_J: float

    interaction_ticks_total: int
    interaction_ticks_completed: int

    movement_budget_per_tick_J: float
    movement_budget_per_tick_m: float
    movement_spent_J: float = 0.0
    movement_spent_m: float = 0.0

    distance_traveled_m: float = 0.0
    distance_traveled_fields: float = 0.0

    harvested_DM_kg: float = 0.0
    assimilated_J: float = 0.0



