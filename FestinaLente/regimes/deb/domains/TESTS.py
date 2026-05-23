

from FestinaLente.regimes.deb.domains.Test_agent_snap import AgentSnapshotT
from FestinaLente.regimes.deb.domains.deb_agent.phases.growth import compute_growth
from FestinaLente.regimes.deb.domains.deb_agent.phases.maintenance import SheepMaintenanceCosts
from FestinaLente.regimes.deb.domains.deb_agent.phases.flux import SheepFluxes
from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState, agent_state_init
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


from FestinaLente.regimes.deb.domains.agent_deb_test import TestAgentDay


def test_reserve_increases_when_grass_is_available():
    ...


def test_structure_increases_when_somatic_surplus_exists() -> None:
    agent = TestAgentDay()
    before = AgentSnapshotT.from_agent(agent)
    agent.early_day_tick()
    agent.late_day_tick()
    after = AgentSnapshotT.from_agent(agent)    
    print(transition_report(before, after))

    return None
    


def test_larger_sheep_has_larger_movement_cost():
    ...


def test_larger_sheep_has_larger_maintenance_cost():
    ...


def test_juvenile_reaches_adult_under_abundant_food():
    ...


def test_adult_accumulates_reproduction_buffer():
    ...


def test_adult_reproduces_when_buffer_is_filled():
    ...


def test_sheep_dies_when_costs_cannot_be_paid():
    ...




def transition_report(before: AgentSnapshotT, after: AgentSnapshotT) -> str:
    dE = after.E_J - before.E_J
    dV = after.V_cm3 - before.V_cm3
    dEH = after.E_H_J - before.E_H_J

    return "\n".join([
        "STATE TRANSITION",
        f"  reserve: {fmt_j(before.E_J)} -> {fmt_j(after.E_J)} ({fmt_j(dE)})",
        f"  structure: {before.V_cm3:.4f} -> {after.V_cm3:.4f} cm³ ({dV:+.6f})",
        f"  maturity: {fmt_j(before.E_H_J)} -> {fmt_j(after.E_H_J)} ({fmt_j(dEH)})",
    ])

def fmt_j(value: float) -> str:
    """Human-readable joule formatter."""
    abs_v = abs(value)

    if abs_v >= 1_000_000:
        return f"{value / 1_000_000:.3f} MJ"
    if abs_v >= 1_000:
        return f"{value / 1_000:.1f} kJ"
    return f"{value:.2f} J"


def fmt_pct(value: float) -> str:
    return f"{100.0 * value:.1f}%"


def safe_ratio(num: float, den: float) -> float:
    if den == 0:
        return float("inf") if num > 0 else 1.0
    return num / den


def pass_fail_ratio(paid: float, due: float) -> str:
    ratio = safe_ratio(paid, due)

    if ratio >= 1.0:
        return f"PASS {fmt_pct(1.0)}"
    return f"FAIL {fmt_pct(ratio)}"


def bool_flag(value: bool) -> str:
    return "YES" if value else "NO"

class AgentTest:
    def __init__(
            self,
            agent_id: int,
            agent_taxon: SheepTaxon, 
            filling_ratio: float = 1.0
            ) -> None:
        
        self.state: SheepAgentState = agent_state_init(
            agent_id=agent_id, 
            agent_taxon=agent_taxon,
            filling_ratio=filling_ratio
            )
        
        self.agent_taxon: SheepTaxon = agent_taxon
        self.age_d : int = 0
        self.day_fluxes: SheepFluxes

    def __repr__(self) -> str:
            return (
                f"AgentTest("
                f"id={self.state.agent_id!r}, "
                f"age_d={self.age_d}, "
                f"E_J={self.state.E_J:.3f}, "
                f"V_cm3={self.state.V_cm3:.3f}, "
                f"E_H_J={self.state.E_H_J:.3f}"
                f")"
            )

    def __str__(self) -> str:
        return (
            f"SheepAgent[{self.state.agent_id}] "
            f"age={self.age_d}d | "
            f"V={self.state.V_cm3:.2f} cm³ | "
            f"L={self.state.V_cm3 ** (1/3):.2f} cm | "
            f"E={fmt_j(self.state.E_J)} | "
            f"E_H={fmt_j(self.state.E_H_J)}"
    )


    def debug_report(self, title: str = "AGENT REPORT") -> str:
        lines: list[str] = []

        lines.append("=" * 72)
        lines.append(title)
        lines.append("-" * 72)
        lines.append(str(self))

        if not hasattr(self, "day_fluxes"):
            lines.append("No flux data computed yet.")
            return "\n".join(lines)

        flux = self.day_fluxes
        costs = self.maintenance_costs
        budget = self.interaction_budget

        soma_coverage = safe_ratio(
            costs.somatic_maintenance_paid_J,
            costs.somatic_maintenance_due_J,
        )
        maturity_coverage = safe_ratio(
            costs.maturity_maintenance_paid_J,
            costs.maturity_maintenance_due_J,
        )

        interaction_unlocked = budget.somatic_reserve > 0

        lines.append("")
        lines.append("ENERGY FLUX")
        lines.append(
            f"  mobilized: {fmt_j(flux.mobilized_J)} | "
            f"soma κ: {fmt_j(flux.soma_budget_J)} | "
            f"maturity/repro: {fmt_j(flux.maturity_repro_budget_J)} | "
            f"assimilation: {fmt_j(flux.assimilation_J)}"
        )

        lines.append("")
        lines.append("MAINTENANCE")
        lines.append(
            f"  soma: {pass_fail_ratio(costs.somatic_maintenance_paid_J, costs.somatic_maintenance_due_J)} | "
            f"paid {fmt_j(costs.somatic_maintenance_paid_J)} / "
            f"due {fmt_j(costs.somatic_maintenance_due_J)} | "
            f"deficit {fmt_j(costs.somatic_deficit_J)} | "
            f"surplus {fmt_j(costs.soma_surplus_after_maintenance_J)}"
        )
        lines.append(
            f"  maturity: {pass_fail_ratio(costs.maturity_maintenance_paid_J, costs.maturity_maintenance_due_J)} | "
            f"paid {fmt_j(costs.maturity_maintenance_paid_J)} / "
            f"due {fmt_j(costs.maturity_maintenance_due_J)} | "
            f"deficit {fmt_j(costs.maturity_deficit_J)} | "
            f"surplus {fmt_j(costs.maturity_surplus_after_maintenance_J)}"
        )

        lines.append("")
        lines.append("INTERACTION BUDGET")
        lines.append(
            f"  unlocked: {bool_flag(interaction_unlocked)} | "
            f"total soma: {fmt_j(budget.somatic_reserve)} | "
            f"per interaction tick: {fmt_j(budget.per_tick_movement_reserve)} | "
            f"maturation buffer: {fmt_j(budget.maturation_reserve)} | "
            f"ticks: {budget.delta_t}"
        )

        lines.append("")
        lines.append("DIAGNOSTIC FLAGS")
        lines.append(f"  soma coverage: {fmt_pct(soma_coverage)}")
        lines.append(f"  maturity coverage: {fmt_pct(maturity_coverage)}")
        lines.append(f"  interaction possible: {bool_flag(interaction_unlocked)}")

        return "\n".join(lines)









##################################
    def early_day_tick(self) -> None:
        """ compute fluxes and maintenance costs for the day, before interactions. """
        
        self.maintenance_costs: SheepMaintenanceCosts = compute_maintenance(
            taxon=self.agent_taxon,
            state=self.state,
            fluxes=self.day_fluxes,
            dt=1
        )
        self.interaction_budget: InteractionBudget = get_interaction_reserve(
            maintenance_costs=self.maintenance_costs,
            delta_t=4
        )
        self.interaction_budget.max_locomotion_distance_m = compute_max_locomotion_distance_m(
            somatic_energy_J=self.interaction_budget.somatic_reserve,
            c_transport_J_per_kg_m=self.agent_taxon.baseline_c_transport_J_per_kg_m,
            body_mass_kg=self.state.body_mass_kg,
            terrain_factor=1.0
        )
        self.interaction_budget.max_distance_per_tick_m = self.interaction_budget.max_locomotion_distance_m / self.interaction_budget.delta_t
        

    def interaction_tick(self) -> tuple[float, float]:
        """ compute interactions and deduct costs from s_b, harvest etc. """
        # pick amount of distance traveled and deduct cost from somatic reserve
        traveled = max(self.interaction_budget.max_distance_per_tick_m/2, 0.0)  # placeholder for actual movement decision logic
        movement_cost_J = traveled * self.agent_taxon.baseline_c_transport_J_per_kg_m * self.state.body_mass_kg
        self.interaction_budget.somatic_reserve -= movement_cost_J
        
        return traveled, movement_cost_J

    def late_day_tick(self) -> None:
        """  compute growth, maturation, Assimilation, reproduction, and death. """
        growth_results = compute_growth(
            interaction_result=self.interaction_budget,
            state_V_cm3=self.state.V_cm3,
            taxon_E_G_J_per_cm3=self.agent_taxon.E_G_J_per_cm3
        )
        self.state.V_cm3 = growth_results.V_next_cm3
        self.state.E_H_J += self.interaction_budget.maturation_reserve
        self.age_d += 1



        pass    


















#################################################################################

#test_states()

def test_agent_models() -> None:

    created_agents: list[AgentTest] = []
    test_taxon = SheepTaxon()


    for e in [0.01, 0.1, 0.2, 0.5, 1.0]:
        agent_state = AgentTest(agent_id=e, agent_taxon= test_taxon, filling_ratio=e)
        created_agents.append(agent_state)


    for agent in created_agents: 
        
        before1: AgentSnapshotT = AgentSnapshotT.from_agent(agent)
        agent.early_day_tick()
        agent.late_day_tick()
        after1: AgentSnapshotT = AgentSnapshotT.from_agent(agent)

        print(agent.debug_report("POST EARLY DAY TICK"))
        print(transition_report(before1, after1))


        before2: AgentSnapshotT = AgentSnapshotT.from_agent(agent)
        agent.early_day_tick()
        agent.late_day_tick()
        after2: AgentSnapshotT = AgentSnapshotT.from_agent(agent)
        print(agent.debug_report("POST SECOND EARLY DAY TICK"))
        print(transition_report(before2, after2))

def test_agent_model(day_count : int = 1) -> None:
    
    agent_taxon = SheepTaxon()
    agent = AgentTest(agent_id=1, agent_taxon=agent_taxon, filling_ratio=0.6)
    before: AgentSnapshotT = AgentSnapshotT.from_agent(agent)
    
    for day in range(day_count):
        agent.early_day_tick()
        if day == 1:
            print(agent.debug_report("POST EARLY DAY TICK"))
        traveled, cost = agent.interaction_tick()
        print(f"Traveled {traveled:.2f} m at a cost of {fmt_j(cost)}")
        agent.late_day_tick()

    after: AgentSnapshotT = AgentSnapshotT.from_agent(agent)
    print("" * 72)
    print(agent.debug_report("POST LATE DAY TICK"))

    print("\n" + "=" * 72)
    print(transition_report(before, after))
    

if __name__ == "__main__":
    #test_agent_model(day_count=10)
    test_structure_increases_when_somatic_surplus_exists()