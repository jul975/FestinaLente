
from dataclasses import dataclass


from typing import TYPE_CHECKING
import numpy as np



if TYPE_CHECKING:
        
    from FestinaLente.deb.deb_agent import SheepAgent
    from FestinaLente.deb.deb_state import SheepAgentState
    from FestinaLente.empirical_data.sheep import SheepTaxon    
    
    from FestinaLente.deb.deb_rules import MaintenanceRapport




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




#########################




@dataclass(frozen=True)
class FluxesLedger:
    """
    Tick-level energy fluxes.

    Convention:
    - fields ending in _per_d are powers/rates.
    - fields ending in _J are amounts over the current tick.
    """

    dt_d: float

    L_cm: float
    # cm.
    # Formula: L = max(V, V_min)^(1/3)

    body_mass_kg: float
    # kg.
    # Approx wet mass used for movement.

    p_C_J_per_d: float
    # J / day.
    # Formula: p_C = E * v / L

    mobilized_J: float
    # J.
    # Formula: M = min(E, p_C * dt)

    soma_budget_J: float
    # J.
    # Formula: B_S = kappa * mobilized_J

    maturity_repro_budget_J: float
    # J.
    # Formula: B_H = (1 - kappa) * mobilized_J

    assimilation_J: float
    # J.
    # Formula scaffold: A = kap_X * harvested_food_energy_J




def compute_fluxes(
    state: "SheepAgentState",
    taxon: SheepTaxon,
    assimilation_J: float,
    dt_d: float,
) -> FluxesLedger:
    V_safe = max(state.V_cm3, taxon.V_min_cm3)
    L_cm = V_safe ** (1.0 / 3.0)

    body_mass_kg = max(
        V_safe / 1000.0,
        taxon.min_body_mass_kg,
    )

    p_C = max(state.E_J * taxon.v_cm_per_d / L_cm, 0.0)
    mobilized_J = min(state.E_J, p_C * dt_d)
    soma_budget_J = taxon.kappa * mobilized_J
    maturity_repro_budget_J = (1.0 - taxon.kappa) * mobilized_J

    return FluxesLedger(
        dt_d=dt_d,
        L_cm=L_cm,
        body_mass_kg=body_mass_kg,
        p_C_J_per_d=p_C,
        mobilized_J=mobilized_J,
        soma_budget_J=soma_budget_J,
        maturity_repro_budget_J=maturity_repro_budget_J,
        assimilation_J=assimilation_J,
    )


#####################################################









################################################################
#           USABLE ENERGY FRACTIONS
################################################################


@dataclass
class EnergyLedger:
    mobilized_J: float
    soma_after_maintenance_J: float
    maturity_after_maintenance_J: float


    # isolate maintenance logic while creating the energy ledger instance?




def compute_energy_ledger(maintenanceR: "MaintenanceRapport") -> EnergyLedger:
    return EnergyLedger(
        mobilized_J=maintenanceR.c_j,
        soma_after_maintenance_J=maintenanceR.soma_surplus_after_maintenance_J,
        maturity_after_maintenance_J=maintenanceR.maturity_surplus_after_maintenance_J
    )

###############################################
#                MOVEMENT
###############################################
def _max_movement_range_j(agent : "SheepAgent") -> float: 
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






################################################################
#                  CONTAINER OBJECT
################################################################



@dataclass
class AgentDayLedger:
    """
    1. What did this agent have available today?
    2. What was paid to mandatory maintenance?
    3. What remained available for movement / growth / maturity / reproduction?
    4. What happened during interaction ticks?
    5. What state changes should be applied at day close?
    """
    agent_id: int
    biological_day: int

    fluxes: "FluxesLedger"
    maintenance: "MaintenanceRapport"
    energy: EnergyLedger
    movement: MovementLedger

    interaction_ticks_total: int
    interaction_ticks_completed: int = 0

    movement_spent_J: float = 0.0
    movement_spent_m: float = 0.0
    distance_traveled_m: float = 0.0
    harvested_DM_kg: float = 0.0
    assimilated_J: float = 0.0

    def print_summary(self) -> None:
        print(f"  Mobilized energy: {self.energy.mobilized_J:.1f} J")
        print(f"  Soma after maintenance: {self.energy.soma_after_maintenance_J:.1f} J")
        print(f"  Maturity after maintenance: {self.energy.maturity_after_maintenance_J:.1f} J")





def create_day_ledger(
    agent_id: int,
    biological_day: int,
    agent: "SheepAgent",
    fluxes: "FluxesLedger",
    maintenance: "MaintenanceRapport",
    n_interaction_ticks: int,
) -> AgentDayLedger:
    energy = compute_energy_ledger(
        fluxes=fluxes,
        maintenance=maintenance,
    )

    movement = compute_movement_ledger(
        agent=agent,
        day_len=n_interaction_ticks,
        energy_ledger=energy,
    )

    return AgentDayLedger(
        agent_id=agent_id,
        biological_day=biological_day,
        fluxes=fluxes,
        maintenance=maintenance,
        energy=energy,
        movement=movement,
        interaction_ticks_total=n_interaction_ticks,
    )


#########################################################################
# Movement ledger




#########################################################################
# interaction|harvest ledger



#########################################################################
# 


