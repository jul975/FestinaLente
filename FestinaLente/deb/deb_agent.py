""" 
Object that owns state and delegates behavior

"""

from FestinaLente.deb.deb_state import AgentDerived, SheepAgentState, agent_state_init, derive_sheep_taxon
from FestinaLente.empirical_data.sheep import SheepTaxon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from FestinaLente.deb.deb_ledger import AgentDayLedger
    from FestinaLente.deb.deb_flux import SheepFluxes


class AnimalSpecies:
    '''
    Species-level DEB parameters and derived quantities.
    These are shared across all agents of the same species.
    keeps track of per species count 
    '''

    def __init__(self, taxon: str) -> None:
        print(f"Initializing species with taxon: {taxon}")
        self.taxon: SheepTaxon = SheepTaxon()  # for now, we only have one taxon, so we can ignore the input taxon string and just use the sheep taxon. In the future, we can expand this to support multiple taxa.
        self.derived: AgentDerived = derive_sheep_taxon(self.taxon)
        self.count: int = 0
        self.instance_dict: dict[int, 'SheepAgent'] = {}


    def add_agent_instance(self, agent: 'SheepAgent') -> None:
        if agent.agent_id in self.instance_dict:
            raise ValueError(f"Agent ID {agent.agent_id} already exists in instance_dict.")
        self.instance_dict[agent.agent_id] = agent

    def create_agent(self, agent_id: int) -> 'SheepAgent':
        self.count += 1
        return SheepAgent(agent_id=agent_id, species_obj=self)
    

    def create_agent_series(self, num_agents: int) -> int:

        for i in range(num_agents):
            agent_id = self.count + 1  # generate a new agent ID
            print("")
            print(f"Creating agent with ID: {agent_id}")
            print("")
            new_agent: SheepAgent = self.create_agent(agent_id)
            print(f"Created agent: ")
            new_agent.params_describe()
            self.add_agent_instance(new_agent)


        return self.count



    def check_agent_count(self) -> int:
        return self.count
    
    def iterate_describe_agents(self) -> None:
        for agent_id, agent in self.instance_dict.items():
            if agent_id != agent.agent_id:
                raise ValueError(f"Agent ID mismatch: {agent_id} != {agent.agent_id}")
            
            print("\n")
            print("\n")
            print(f"--- Agent ID: {agent_id} ---")
            agent.params_describe()
            print("\n")




class SheepAgent():
    '''
    Agent object that owns state and delegates behavior.
    rng logic can be implemented here to keep it isolated on the agent level.
    '''

    def __init__(self, agent_id: int, species_obj : AnimalSpecies) -> None:
        self.agent_id: int = agent_id

        self.species_obj: AnimalSpecies = species_obj

        self.position: tuple[float, float] = (0.0, 0.0)

        self.state: SheepAgentState  = agent_state_init(
            agent_id=agent_id,
            species_obj=self.species_obj,
            filling_ratio=1.0
        )

        ## rng placeholder
        

        self.derived: AgentDerived = species_obj.derived
        self.taxon: SheepTaxon = species_obj.taxon

    def params_describe(self) -> None:
        print(f"--- SheepAgent (id={self.agent_id}) ---")
        print("State: ")
        print(self.state)
        print("Derived: ")
        print(self.derived)
        print("Position: ")
        print(self.position)

    def fetch_fluxes(self, assimilation_J: float, dt_d: float = 4.0) -> None:
        from FestinaLente.deb.deb_flux import compute_fluxes
        self.day_fluxes: "SheepFluxes" = compute_fluxes(
            state=self.state,
            taxon=self.taxon,
            assimilation_J=assimilation_J,
            dt_d=dt_d
        )

    def fetch_ledger(self, biological_day: int) -> None:
        if not hasattr(self, "day_fluxes"):
            raise ValueError("Fluxes must be computed before fetching ledger.")
        
        from FestinaLente.deb.deb_ledger import create_day_ledger
        self.day_ledger: "AgentDayLedger" = create_day_ledger(
            agent_id=self.agent_id,
            biological_day=biological_day,
            fluxes=self.day_fluxes,
            agent=self
        )
    
    # 1. start of day tick: fetch fluxes and create day ledger, perform maintenance and update day ledger accordingly
    # 2. interaction tick: perform movement, harvest and interactions, update day ledger accordingly
    # 3. end of day tick: apply growth, maturity, reproduction, and death based on day ledger






if __name__ == "__main__":
    print("Testing sheep agent:")
    sheep_species = AnimalSpecies(taxon="sheep")
    sheep_species.create_agent_series(num_agents=3)
    print(f"Total sheep count: {sheep_species.check_agent_count()}")


    agent_1 = sheep_species.instance_dict[1]
    agent_1.fetch_fluxes(assimilation_J=1000.0, dt_d=4.0)
    print(f"Agent 1 fluxes: ")
    print(agent_1.day_fluxes)
    print("\n")

    agent_1.fetch_ledger(biological_day=1)
    print(f"Agent 1 day ledger: ")
    agent_1.day_ledger.print_summary()