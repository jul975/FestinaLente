



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

def test_states() -> None:

    created_agents: list[type[SheepAgentState]] = []


    for e in [0.01, 0.1, 0.2, 0.5, 1.0]:
        



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
            taxon=agent_taxon,
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

        maintance_cost: SheepMaintenanceCosts = compute_maintence(taxon=agent_taxon, state=agent, fluxes=fluxes)

        print("")
        print('MAINTEN')
        print(maintance_cost)

        






