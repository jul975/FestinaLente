



"""def test_reserve_increases_when_grass_is_available():
    ...


def test_structure_increases_when_somatic_surplus_exists():
    ...


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
    ..."""

from FestinaLente.regimes.deb.domains.deb_agent.agent_maintenance import SheepMaintenanceCosts, compute_maintenance
from FestinaLente.regimes.deb.domains.deb_agent.agent_flux import SheepFluxes, compute_fluxes
from FestinaLente.regimes.deb.domains.deb_agent.agent_reserve import InteractionBudget, InteractionBudget, get_interaction_reserve
from FestinaLente.regimes.deb.domains.deb_agent.agent_state import SheepAgentState, agent_state_init
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


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
        
        self.age_d : int = 0
        
        pass


def test_states() -> None:

    created_agents: list[type[SheepAgentState]] = []
    test_taxon = SheepTaxon()


    for e in [0.01, 0.1, 0.2, 0.5, 1.0]:
        agent_state: SheepAgentState = agent_state_init(agent_id=e, agent_taxon= test_taxon, filling_ratio=e)
        created_agents.append(agent_state)

    for agent in created_agents:

        print()
        print("===============")
        print(f"reserve fill ratio = {agent.agent_id}")
        print(f"structural volume = {agent.V_cm3} cm3")
        print(f"E_reserve = {agent.E_J} J")
        print(f"Maturity = {agent.E_H_J}")

     
        fluxes: SheepFluxes = compute_fluxes(
            state = agent,
            taxon=test_taxon,
            assimilation_J= 0, 
            dt_d=1)
        
        print("")
        print("FLUX DATA")
        print(fluxes.dt_d, "dt")
        print(fluxes.L_cm, "L_cm")
        print(fluxes.body_mass_kg, "body_mass")
        print(fluxes.p_C_J_per_d, "pC")
        print(fluxes.mobilized_J, "mobilized_J")
        print(fluxes.soma_budget_J, "soma_budget_j")
        print(fluxes.maturity_repro_budget_J, "maturity_repro_budget_j")
        print(fluxes.assimilation_J, "assimilation")

        maintance_cost: SheepMaintenanceCosts = compute_maintenance(taxon=test_taxon, state=agent, fluxes=fluxes)

        print("")
        print('MAINTEN')
        print(maintance_cost)
        print()
        print("soma reserve for interactions",maintance_cost.soma_surplus_after_maintenance_J)
        print("maturity reserve:", maintance_cost.maturity_surplus_after_maintenance_J)
 

        interaction_r: InteractionBudget = get_interaction_reserve(maintance_cost, 4)
        print()
        print(f"interaction dt: {interaction_r.delta_t}")
        print(f"interaction somatic r: {interaction_r.somatic_reserve}")
        print(f"interaction per tick: {interaction_r.per_tick_movement_reserve}")
        print(f"interaction maturity: {interaction_r.maturation_reserve}")
        print("====================================")
test_states()




