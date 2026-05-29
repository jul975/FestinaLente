
from dataclasses import dataclass


from typing import TYPE_CHECKING
import numpy as np



if TYPE_CHECKING:
        
    from FestinaLente.core.fluxes.agent_flux import AgentFluxes
    from FestinaLente.deb.deb_agent import SheepAgent
    from FestinaLente.deb.deb_state import SheepAgentState
    from FestinaLente.empirical_data.sheep import SheepTaxon    
    
from FestinaLente.deb.deb_rules import brockway_boyne_c_transport




#####################################

def fmt_j(value: float) -> str:
    """Format joules into readable energy units."""
    abs_value = abs(value)

    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.3f} MJ"
    if abs_value >= 1_000:
        return f"{value / 1_000:.1f} kJ"
    return f"{value:.2f} J"


def fmt_m(value: float) -> str:
    """Format meters into readable movement units."""
    if abs(value) >= 1_000:
        return f"{value / 1_000:.2f} km"
    return f"{value:.2f} m"


class LedgerFormatMixin:
    """
    Shared formatting protocol for ledger-style dataclasses.

    Supported usage:
        str(obj)
        format(obj, "report")
        format(obj, "compact")
        f"{obj:report}"
    """

    def __str__(self) -> str:
        return format(self, "report")

    def __format__(self, spec: str) -> str:
        spec = spec or "report"

        if spec == "report":
            return "\n".join(self._format_report_lines())

        if spec == "compact":
            return self._format_compact()

        if spec == "debug":
            return repr(self)

        raise ValueError(
            f"Unknown format spec {spec!r} for {type(self).__name__}. "
            "Expected: 'report', 'compact', or 'debug'."
        )

    def _format_report_lines(self) -> list[str]:
        return [repr(self)]

    def _format_compact(self) -> str:
        return repr(self)
















################################################################
@dataclass(frozen=True)
class MaintenanceCostsLedger:
    """
    Tick-level maintenance accounting.

    Maintenance has priority over growth and maturation.
    """

    c_j: float 
    # c_j

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

def compute_maintenance(
            taxon : 'SheepTaxon', 
            state : 'SheepAgentState' ,
            fluxes : 'AgentFluxes', 
            dt: float = 1.0 
            ) -> MaintenanceCostsLedger:
        """ compute maintenance costs and deficits for the current tick, given the agent state, taxon parameters, and available fluxes for the tick.        
            somatic maintenance => cost of maintaining existing structure 
                depends on how much structure there is (V) and how costly it is to maintain per unit of structure (p_M)
            maturity maintenance => cost of maintaining maturity level 
                depends on how much maturity there is (E_H) and how costly it is to maintain per unit of maturity (k_J)
            """
        
        somatic_maintenance: float = taxon.p_M_J_per_d_cm3 * state.V_cm3 * dt
        c_j: float = taxon.k_J_per_d * state.E_H_J *dt

        return MaintenanceCostsLedger(
            c_j=c_j,

            somatic_maintenance_due_J=somatic_maintenance,
            somatic_maintenance_paid_J=min(somatic_maintenance, fluxes.soma_budget_J),
            somatic_deficit_J=max(somatic_maintenance-fluxes.soma_budget_J, 0),
            soma_surplus_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintenance, 0),

            maturity_maintenance_due_J= c_j,
            maturity_maintenance_paid_J=min(c_j, fluxes.maturity_repro_budget_J),
            maturity_deficit_J=max(c_j-fluxes.maturity_repro_budget_J, 0),
            maturity_surplus_after_maintenance_J=max(fluxes.maturity_repro_budget_J-c_j, 0)



        )

@dataclass
class EnergyLedger:
    mobilized_J: float
    soma_after_maintenance_J: float
    maturity_after_maintenance_J: float


    # isolate maintenance logic while creating the energy ledger instance?

def compute_energy_ledger(maintenanceR: MaintenanceCostsLedger) -> EnergyLedger:
    return EnergyLedger(
        mobilized_J=maintenanceR.c_j,
        soma_after_maintenance_J=maintenanceR.soma_surplus_after_maintenance_J,
        maturity_after_maintenance_J=maintenanceR.maturity_surplus_after_maintenance_J
    )

###############################################

def _max_movement_range_j(agent : SheepAgent) -> float: 
    """
    compute max movement range to J (without terrain correction)
    s_t = D_{max}(c_transport * mass * tau)
    """
    c_transport: float = agent.taxon.c_transport_flat_J_per_kg_m
    body_mass_gram: float = agent.state.body_mass_kg * 1000 
    d_max : float = agent.taxon.baseline_daily_path_length_m
    return c_transport * body_mass_gram * d_max


@dataclass(frozen=True)
class MovementLedger:
    '''
    input ready dataclass for interaction pipelines
    NOTE:
        terrain factor TAU has NOT been added, should be done locally for the interaction tick FIRST
    '''
    emp_max_movement_j_tau_neg : float
    emp_max_tick_movement_j_tau_neg: float

    correction_ratio: float

    soma_per_tick_j:float


def compute_movement_ledger(agent:'SheepAgent', day_len: int, energy_ledger:EnergyLedger)->MovementLedger:
    '''
    needs ready to go movement input to make separations clear, 
    # length of the days
    # post-maintenance reserve evaluation => weight for the movement logic
    # 
    # 
    
    '''
    usable_soma : float = energy_ledger.soma_after_maintenance_J
    
    max_move_range_j: float = _max_movement_range_j(max_distance=agent.taxon.baseline_daily_path_length_m ,c_transport= agent.taxon.c_transport_flat_J_per_kg_m)
    # max range in j can be ratio'ed somatic_branch/max_move
    # NOTE: tau correction on what level => will overshoot here but will be later fix

    

    correction_ratio : float = usable_soma/max_move_range_j

    per_tick_budget_j : float = max_move_range_j/day_len

    soma_per_tick_j : float = usable_soma/day_len


    return MovementLedger(
        emp_max_movement_j_tau_neg=max_move_range_j,
        emp_max_tick_movement_j_tau_neg=per_tick_budget_j,
        correction_ratio=correction_ratio,
        soma_per_tick_j=soma_per_tick_j
    )


def execute_movement(agent:'SheepAgent', movement_ledger:MovementLedger, terrain_factor : float = 1.0):

    # evaluate what range to use using correction Ratio, 
    if movement_ledger.correction_ratio < 1:
        print("deficient interaction phase")


    # draw movement distance and correct for terrain factor
    rng: np.random.Generator = agent.rng
    rng.

    
    # need to use basic geomitry to check for non linear vs linear movement 





    return 








@dataclass
class AgentDayLedger:
    """ 
    Created by DAY_OPEN tick, 
    updated during interaction ticks, 
    and used in DAY_CLOSE tick to apply growth, maturity, reproduction, and death.
    """
    agent_id: int
    biological_day: int

    

    interaction_ticks_total: int
    interaction_ticks_completed: int


    max_movement_range_j : float


    movement_budget_per_tick_J: float
    #movement_budget_per_tick_m: float
    movement_spent_J: float = 0.0
    movement_spent_m: float = 0.0

    distance_traveled_m: float = 0.0
    distance_traveled_fields: float = 0.0

    harvested_DM_kg: float = 0.0
    assimilated_J: float = 0.0

    # need movement ledger obj

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
    fluxes: "AgentFluxes",
    agent: "SheepAgent",
    n_interaction_ticks: int = 4,  # assuming 4 ticks per day for simplicity
) -> AgentDayLedger:
    """ create day ledger for an agent at the start of the day, with initial values based on fluxes and agent state """

    kappa: float = agent.taxon.kappa

    somatic_maintenance: float = kappa * fluxes.mobilized_J
    c_j: float = (1 - kappa) * fluxes.mobilized_J

    



    # need availability/max_distance_cost for correction. 
    # can be used with probability's to mimic exhaustion

    return AgentDayLedger(
        agent_id=agent_id,
        biological_day=biological_day,

        mobilized_J=fluxes.mobilized_J,
        soma_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintenance, 0),
        maturity_after_maintenance_J=max(fluxes.maturity_repro_budget_J - c_j, 0),
        interaction_ticks_total=0,
        interaction_ticks_completed=0,
        #
        movement_budget_per_tick_J=movement_budget_per_tick_J,  
        #
        movement_budget_per_tick_m=movement_budget_per_tick_M
    )



#########################################################################
# Movement ledger




#########################################################################
# interaction|harvest ledger



#########################################################################
# 


