





from dataclasses import dataclass

from FestinaLente.regimes.deb.universal_laws.agent_phases import BranchBudget, MaintenanceResult, MobilizationResult, begin_day_energy_phase, branch_split_phase, maintenance_phase


def early_day_energy_update(state, params, dt: float):
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

    self.early_tick_energy_update(dt)

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
class DailyStateParams:
    """Contains all computed values and derivations for the rest of the day"""
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
    return p_C #* dt