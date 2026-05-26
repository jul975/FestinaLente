

from FestinaLente.deb.deb_agent import AnimalSpecies, SheepAgent


def test_sheep_agent_series() -> None:

    print("Testing sheep agent:")
    sheep_species = AnimalSpecies(taxon="sheep")
    sheep_species.create_agent_series(num_agents=3)
    print(f"Total sheep count: {sheep_species.check_agent_count()}")

def test_sheep_agent_fluxes_and_ledger() -> None:
    print("Testing sheep agent fluxes and ledger:")
    sheep_species = AnimalSpecies(taxon="sheep")
    sheep_species.create_agent_series(num_agents=3)
    agent_1: SheepAgent = sheep_species.instance_dict[1]
    agent_1.fetch_fluxes_ledger(assimilation_J=1000.0, dt_d=4.0)
    print(f"Agent 1 fluxes: ")
    print(agent_1.day_fluxes)
    print("\n")

    agent_1.fetch_new_ledger(biological_day=1)
    print(f"Agent 1 day ledger: ")
    agent_1.day_ledger.print_summary()


if __name__ == "__main__":
    
    print("=================================================================")
    test_sheep_agent_series()
    print("\n")
    print("=================================================================")
    print("\n")
    test_sheep_agent_fluxes_and_ledger()
    
    print("=================================================================")