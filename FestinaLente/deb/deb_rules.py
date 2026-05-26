
from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FestinaLente.deb.deb_agent import SheepAgent
    from FestinaLente.deb.deb_state import SheepAgentState
    from FestinaLente.core.fluxes.agent_flux import AgentFluxes
    from FestinaLente.empirical_data.sheep import SheepTaxon


'''

state_t → energy ledger → state_t+1


E = total reserve energy, J
V = structural volume, cm³
L = structural length = V^(1/3), cm
[E] = reserve density = E / V, J/cm³
r = specific growth rate, 1/day => daily relative increase in structural volume
v / L = reserve turnover/conductance rate, 1/day



'''



@dataclass(frozen=True)
class MaintenanceCostsLedger:
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

def compute_maintenance(
            taxon : 'SheepTaxon', 
            state : 'SheepAgentState' ,
            fluxes : AgentFluxes, 
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
            somatic_maintenance_due_J=somatic_maintenance,
            somatic_maintenance_paid_J=min(somatic_maintenance, fluxes.soma_budget_J),
            somatic_deficit_J=max(somatic_maintenance-fluxes.soma_budget_J, 0),
            soma_surplus_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintenance, 0),

            maturity_maintenance_due_J= c_j,
            maturity_maintenance_paid_J=min(c_j, fluxes.maturity_repro_budget_J),
            maturity_deficit_J=max(c_j-fluxes.maturity_repro_budget_J, 0),
            maturity_surplus_after_maintenance_J=max(fluxes.maturity_repro_budget_J-c_j, 0)



        )

##############################################################################

@dataclass(frozen=True)
class LocomotionCostSpec:
    """
    c_{transport}​(G,S)=2.35+0.398G+0.0286G^2−0.036S+0.00052S^2
    """
    source: str = "Brockway_Boyne_1980_sheep"
    mode: str = "scalar_fallback"  # or "slope_speed_regression"
    baseline_c_transport_J_per_kg_m: float = 2.35



def brockway_boyne_c_transport(
    gradient_degrees: float,
    speed_m_per_min: float,
) -> float:
    """ NOTE: later implementation """
    return (
        2.35
        + 0.398 * gradient_degrees
        + 0.0286 * gradient_degrees**2
        - 0.036 * speed_m_per_min
        + 0.00052 * speed_m_per_min**2
    )




##############################################################################



@dataclass(frozen=True)
class DayOpenTickReport:
    biological_day: int
    n_agents_processed: int
    total_mobilized_J: float
    total_somatic_maintenance_due_J: float
    total_somatic_maintenance_paid_J: float
    total_maturity_maintenance_due_J: float
    total_maturity_maintenance_paid_J: float


@dataclass(frozen=True)
class InteractionTickReport:
    biological_day: int
    interaction_index: int
    n_agents_processed: int
    total_distance_m: float
    total_movement_cost_J: float
    total_harvested_DM_kg: float
    total_assimilated_J: float


@dataclass(frozen=True)
class DayCloseTickReport:
    biological_day: int
    n_agents_processed: int
    total_growth_dV_cm3: float
    total_maturity_gain_J: float
    births: int
    deaths: int




##############################################################################








##############################################################################