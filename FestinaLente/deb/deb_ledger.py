
from dataclasses import dataclass
from turtle import distance


from FestinaLente.core.fluxes.agent_flux import AgentFluxes
from FestinaLente.deb.deb_agent import SheepAgent

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

    def print_summary(self) -> None:
        print(f"Agent {self.agent_id} - Day {self.biological_day}")
        print(f"  Mobilized energy: {self.mobilized_J:.1f} J")
        print(f"  Soma after maintenance: {self.soma_after_maintenance_J:.1f} J")
        print(f"  Maturity after maintenance: {self.maturity_after_maintenance_J:.1f} J")
        print(f"  Movement spent: {self.movement_spent_J:.1f} J, {self.movement_spent_m:.2f} m")
        print(f"  Distance traveled: {self.distance_traveled_m:.2f} m")
        print(f"  Harvested DM: {self.harvested_DM_kg:.4f} kg, Assimilated energy: {self.assimilated_J:.1f} J")



def create_day_ledger(
    agent_id: int,
    biological_day: int,
    fluxes: AgentFluxes,
    agent: SheepAgent,
    n_interaction_ticks: int = 4,  # assuming 4 ticks per day for simplicity
) -> AgentDayLedger:
    """ create day ledger for an agent at the start of the day, with initial values based on fluxes and agent state """

    kappa: float = agent.taxon.kappa

    somatic_maintenance = kappa * fluxes.mobilized_J
    c_j = (1 - kappa) * fluxes.mobilized_J

    return AgentDayLedger(
        agent_id=agent_id,
        biological_day=biological_day,

        mobilized_J=fluxes.mobilized_J,
        soma_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintenance, 0),
        maturity_after_maintenance_J=max(fluxes.maturity_repro_budget_J - c_j, 0),
        interaction_ticks_total=0,
        interaction_ticks_completed=0,
        movement_budget_per_tick_J=fluxes.p_C_J_per_d / n_interaction_ticks,  
        movement_budget_per_tick_m=fluxes.p_C_J_per_d / n_interaction_ticks / fluxes.p_C_J_per_d * fluxes.L_cm / 100,  # convert cm to m
    )
