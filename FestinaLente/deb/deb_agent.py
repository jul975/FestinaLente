""" 
Object that owns state and delegates behavior

"""

import numpy as np
from numpy.random import Generator

from FestinaLente.deb.deb_rules import MaintenanceCostsLedger, compute_maintenance
from FestinaLente.deb.deb_state import AgentDerived, SheepAgentState, agent_state_init, derive_sheep_taxon
from FestinaLente.empirical_data.sheep import SheepTaxon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from FestinaLente.deb.deb_ledger import AgentDayLedger
    from FestinaLente.deb.deb_flux import FluxesLedger


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

        # temp
        self.rng : np.random.SeedSequence = np.random.SeedSequence(entropy=agent_id)  # for now, we can use the agent ID as the seed for the random number generator. This will ensure that each agent has a unique and deterministic RNG sequence based on its ID. In the future, we can expand this to support more complex seeding strategies if needed.

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

    def test_rng(self) -> None:
        print(f"Testing RNG for agent {self.agent_id} with seed {self.rng.entropy}")
        rng: Generator = np.random.default_rng(self.rng)
        print("Random numbers: ", rng.random(5))

    def params_describe(self) -> None:
        print(f"--- SheepAgent (id={self.agent_id}) ---")
        print("State: ")
        print(self.state)
        print("Derived: ")
        print(self.derived)
        print("Position: ")
        print(self.position)

    def fetch_fluxes_ledger(self, assimilation_J: float = 0, dt_d: float = 4.0) -> None:
        ''' compute fluxes and store in day_fluxes attribute 
        attributes: 
        - assimilation_J: energy assimilated during the day, in Joules. This is an input to the flux computation, and can be set based on the agent's foraging behavior and the environment. For now, we can set it to 0 and focus on the mobilization and budget split fluxes.
        - dt_d: time step for the flux computation, in days. This can be set to 1 for daily fluxes, or a fraction of a day for sub-daily fluxes. For now, we can set it to 4.0 to represent 4 days, which will allow us to see more significant changes in the fluxes and make it easier to debug and understand the model dynamics.
        '''
        from FestinaLente.deb.deb_flux import compute_fluxes
        self.day_fluxes: "FluxesLedger" = compute_fluxes(
            state=self.state,
            taxon=self.taxon,
            assimilation_J=assimilation_J,
            dt_d=dt_d
        )

    def fetch_new_ledger(self, biological_day: int) -> None:
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

    def perform_maintenance(self) -> MaintenanceCostsLedger:
        if not hasattr(self, "day_ledger"):
            raise ValueError("Day ledger must be created before performing maintenance.")
        
        maintenance_ledger: MaintenanceCostsLedger = compute_maintenance(
            state=self.state,
            taxon=self.taxon,
            fluxes=self.day_fluxes
        )
        self.day_ledger.soma_after_maintenance_J = max(self.day_fluxes.soma_budget_J - maintenance_ledger.somatic_maintenance_J, 0)
        self.day_ledger.maturity_after_maintenance_J = max(self.day_fluxes.maturity_repro_budget_J - maintenance_ledger.maturity_maintenance_due_J, 0)
        return maintenance_ledger

        # # apply maintenance costs to the day ledger
        # self.day_ledger.soma_after_maintenance_J = max(self.day_fluxes.soma_budget_J - self.day_fluxes.p_C_J_per_d, 0)
        # self.day_ledger.maturity_after_maintenance_J = max(self.day_fluxes.maturity_repro_budget_J - (1 - self.taxon.kappa) * self.day_fluxes.p_C_J_per_d, 0)
        # ## temp 


    def start_of_day_tick(self, biological_day: int, assimilation_J: float = 0, dt_d: float = 4.0) -> None:
        """
        instance attributes are being updated in place downstream
        - fetch fluxes and create day ledger
        - perform maintenance and update day ledger accordingly

        """

        self.fetch_fluxes_ledger(assimilation_J=assimilation_J, dt_d=dt_d)
        self.fetch_new_ledger(biological_day=biological_day)
        self.perform_maintenance()

        # needs to create interaction ledger ready for the day!. 


    # 2. interaction tick: perform movement, harvest and interactions, update day ledger accordingly

    def interaction_tick(self) -> None:
        ## add simular logic, need to mimic start of day, passing reports and ledgers between ticks. 
        if not hasattr(self, "day_ledger"):
            raise ValueError("Day ledger must be created before performing interaction tick.")
        if not hasattr(self, "day_fluxes"):
            raise ValueError("Fluxes must be computed before performing interaction tick.")
        if not hasattr(self, "derived"):
            raise ValueError("Derived parameters must be computed before performing interaction tick.")
        
        pass
    # 3. end of day tick: apply growth, maturity, reproduction, and death based on day ledger






if __name__ == "__main__":
    species = AnimalSpecies(taxon="sheep")
    species.create_agent_series(num_agents=3)
    
    test_agent: SheepAgent = species.instance_dict[1]
    test_agent.test_rng()
    print("\n")
    test_agent.test_rng()

    test_2_agent: SheepAgent = species.instance_dict[2]
    test_2_agent.test_rng()
    print("\n")
    test_2_agent.test_rng()
    print("\n")