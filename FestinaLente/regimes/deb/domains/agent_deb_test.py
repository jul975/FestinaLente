#########################################################
#                   AGENT DEB TEST
#########################################################
import numpy
import test

from FestinaLente.regimes.deb.domains.deb_agent.cycle.day_open_tick import open_day_tick
from FestinaLente.regimes.deb.domains.deb_agent.derived import AgentDerived
from FestinaLente.regimes.deb.domains.deb_agent.ledger import AgentDayLedger
from FestinaLente.regimes.deb.domains.deb_agent.phases.growth import SheepGrowthResult, compute_growth
from FestinaLente.regimes.deb.domains.deb_agent.phases.movement import compute_locomotion_cost
from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState, agent_state_init
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon



class TestAgentDay:
    def __init__(self,
                  agent_id: int ,
                  params: SheepTaxon  ) -> None:
        self.params: SheepTaxon = params

        self.rng = numpy.random.default_rng(seed=123)  # create a rng for the agent, seeded by agent id for reproducibility

        self.position = (0.0, 0.0)

        state, derived = agent_state_init(  
            agent_id=agent_id,
            agent_taxon=self.params,
            filling_ratio=1.0
        )

        self.state: SheepAgentState = state
        self.derived: AgentDerived = derived

    def early_day_tick(self) -> AgentDayLedger:
        """pre-movement energy update, which includes mobilization, branch split, maintenance, movement cost deduction, etc. Returns day ledger for the day tick."""
        self.day_ledger: AgentDayLedger = open_day_tick(
            agent_state=self.state, 
            paramsTaxon=self.params, 
            derived=self.derived,
            day_length_d=4.0
        )
        return self.day_ledger

    def day_tick(self) -> AgentDayLedger:
        # use rng to draw on agent level 
        # => can be used to simply pass draws and keep rng's isolated on agent obj
        # => harvest draw 
        # => 2 movement draws (move success, move distance) 
        #           # => need to be integrated to get distance traveled / fields crossed 
                    #    as of now, 100X100 world
                    #    field size : 
    
        
        # fetch max distance traveled 
        max_distance_m = self.day_ledger.movement_budget_per_tick_m
        traveld = self.rng.uniform(0, max_distance_m)
        energy_spend_travel_J = compute_locomotion_cost(
            distance_m=traveld,
            gradient_degrees=0.0,  # flat terrain for now
            speed_m_per_min=50.0,  # arbitrary speed for now
            body_mass_kg=self.state.body_mass_kg
        )
        self.day_ledger.movement_spent_m += traveld
        self.day_ledger.movement_spent_J += energy_spend_travel_J
        self.day_ledger.soma_after_maintenance_J -= energy_spend_travel_J




        return self.day_ledger


    def late_day_tick(self) -> None:
        """
        update state based on day ledger, which includes energy update, position update, etc.
        """
        res: SheepGrowthResult = compute_growth(
            remaining_J=self.day_ledger.soma_after_maintenance_J,
            state_V_cm3=self.state.V_cm3,
            taxon_E_G_J_per_cm3=self.params.E_G_J_per_cm3
        )

        print(f"Growth energy used: {res.growth_energy_J:.2f} J, dV: {res.dV_cm3:.2f} cm3, V_next: {res.V_next_cm3:.2f} cm3"    )
        print(f"Distance traveled: {self.day_ledger.movement_spent_m:.2f} m, Energy spent on movement: {self.day_ledger.movement_spent_J:.2f} J")
        print(f"Total energy spent: {self.day_ledger.movement_spent_J + res.growth_energy_J:.2f} J, Remaining energy: {self.day_ledger.soma_after_maintenance_J - (self.day_ledger.movement_spent_J + res.growth_energy_J):.2f} J")


        self.state.V_cm3 = res.V_next_cm3

        return None





        




if __name__ == "__main__":
    params = SheepTaxon()
    testObj = TestAgentDay(
        agent_id=1,
        params=params
    )

    day_ledger = testObj.early_day_tick()
    print("After early day tick:")
    print(day_ledger)

    testObj.day_tick()
    print("After day tick:")
    print(testObj.day_ledger)

    testObj.late_day_tick()
    print("After late day tick:")
    print(testObj.state)
    



    



