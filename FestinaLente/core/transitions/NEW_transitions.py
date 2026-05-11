





from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.agent_register.agent_flux import daily_somatic_maintenance_J, somatic_maintenance_J
from FestinaLente.regimes.deb.domains.deb_agent.agent_register.agent_phases import BranchBudget, MaintenanceResult, MobilizationResult, begin_day_energy_phase, branch_split_phase, maintenance_phase


def early_day_energy_update(state, params, dt: float) -> None:
    """
    update pre-movement energy steps, e.g. mobilization, branch split, maintenance, movement cost deduction, etc.
    """
    # 0. add assimilation energy to reserve (not implemented yet, so assume constant reserve for now)

    # 1. Mobilization phase
    mobilized_energy: MobilizationResult = begin_day_energy_phase(state=state, params=params, dt=dt)

    # 2. Branch split phase
    branch_budget: BranchBudget = branch_split_phase(mobilized_energy, params)

    # 3. Maintenance phase
    maintenance_result: MaintenanceResult = maintenance_phase(
        state, params, dt, branch_budget
    )

    return

def interaction_phase(self, dt: float):
    """movement phase, which deducts movement cost from soma budget, and returns movement result for use in growth phase."""
    movement_result = movement_phase(
        self, branch_budget.soma_budget_J, self.params, dt
    )
    return movement_result

def end_of_day_state_update(self):
    """
    growth and status update, end with harvest assimilation
    
    """
    pass



def step(self, dt: float):


    # 4. Movement phase (placeholder)
    movement_result = movement_phase(
        self, branch_budget.soma_budget_J, self.params, dt
    )

    # 5. Growth phase
    growth_result = growth_phase(
        self.state,
        branch_budget.soma_budget_J - movement_result.movement_cost_J,
        self.params,
        dt,
    )

    # 6. Maturity/Reproduction phase
    maturity_result = maturity_reproduction_phase(
        self.state, branch_budget.maturity_repro_budget_J, self.params
    )

    # 7. Harvest

    # 8. Update state variables, e.g. age, offspring count, etc.
    self.state += dt
#############################################################################
@dataclass
class DEBAgentState:
    agent_id: int
    parent_id: int | None
    offspring_count: int

    position: tuple[int, int]
    age_days: float
    alive: bool

    E: float       # reserve energy, J
    V: float       # structural volume, cm^3
    E_H: float     # maturity, J
    E_R: float     # reproduction buffer, J


@dataclass(frozen=True)
class PhysiologySpec:
    # mobilization / allocation
    v: float              # cm / day
    kappa: float          # soma allocation
    kappa_R: float        # reproduction efficiency

    # soma
    p_M: float            # J / day / cm^3
    E_G: float            # J / cm^3

    # maturity
    k_J: float            # 1 / day
    E_Hb: float           # J
    E_Hx: float           # J
    E_Hp: float           # J

    # numerical guard
    V_min: float = 1e-6 

@dataclass
class StructureParams:
    """ mid transition computed values:
     - C_S: somatic maint cost per day """
    C_S: float      # J / day / cm^3

    E_G: float      # J / cm^3
    p_T: float = 0  # optional, ignored for now

@dataclass
class DailyStateParams:
    """Contains all computed values and derivations for the rest of the day"""

    pass


def get_movement_cost():
    pass


def morning_energy_compute(agent_state : DEBAgentState, physiology_spec : PhysiologySpec) -> DailyStateParams:
    """ evaluate agent state and create computed anchor for derivations"""

    def structural_length_cm(V: float, V_min: float) -> float:
        """Return structural length L = V^(1/3), in cm."""
        V_safe = max(V, V_min)
        return V_safe ** (1.0 / 3.0)

    def mobilize_power_deb_lite(agent_state: DEBAgentState, params: PhysiologySpec) -> float:
        """
        Mobilized reserve power p_C in J/day.

        DEB-lite version:
            p_C = E_reserve * v / L

        This does not yet include the full DEB growth correction term '- r'.
        """
        L = structural_length_cm(agent_state.V, params.V_min)
        p_C = agent_state.E * params.v / L
        return max(p_C, 0.0)

    p_C: float = mobilize_power_deb_lite(agent_state=agent_state, params=physiology_spec)
    # correct for time step
    # return p_C in J/day, but we will use it for a dt time step, so multiply by dt to get energy available for this time step
    C_S = daily_somatic_maintenance_J(agent_state, physiology_spec)
    B_S = p_C * physiology_spec.kappa
    B_M = p_C * (1-physiology_spec.kappa)

    movement_budget = B_S - C_S

    movement_cost: float = get_movement_cost()
    return p_C #* dt