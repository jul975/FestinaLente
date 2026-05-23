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

    def __str__(self) -> str:
        return f"SheepAgentState( \n agent_id={self.state.agent_id}, \n age_d={self.state.age_d:.2f}, \n alive={self.state.alive}, \n E_J={self.state.E_J:.2f}, \n V_cm3={self.state.V_cm3:.2f}, \n E_H_J={self.state.E_H_J:.2f}, \n E_R_J={self.state.E_R_J:.2f}, \n body_mass_kg={self.state.body_mass_kg:.2f})"

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
        self.state.age_d += 1.0
        #self.state.body_mass_kg = self.state.V_cm3 * self.derived.V_m_cm3 / 1000  # convert g to kg, assuming density of 1 g/cm3 for simplicity

        return None



# in agent_deb_test.py — add to TestAgentDay

    def snapshot(self, label: str, ledger: AgentDayLedger | None = None) -> None:
        sep = f"── {label} "
        print(sep + "─" * max(0, 60 - len(sep)))
        print(f"  V={self.state.V_cm3:.4f} cm³  "
            f"E={self.state.E_J:.1f} J  "
            f"E_H={self.state.E_H_J:.1f} J  "
            f"mass={self.state.body_mass_kg:.3f} kg")
        if ledger:
            print(f"  mobilized={ledger.mobilized_J:.1f} J  "
                f"soma_surplus={ledger.soma_after_maintenance_J:.1f} J  "
                f"maturity_surplus={ledger.maturity_after_maintenance_J:.1f} J")
            print(f"  movement: budget={ledger.movement_budget_per_tick_m:.1f} m/tick  "
                f"spent={ledger.movement_spent_m:.1f} m  ({ledger.movement_spent_J:.1f} J)")
            if ledger.assimilated_J > 0:
                print(f"  assimilated={ledger.assimilated_J:.1f} J  "
                    f"harvested={ledger.harvested_DM_kg:.4f} kg DM")

            




if __name__ == "__main__":
    params = SheepTaxon()
    testObj = TestAgentDay(
        agent_id=1,
        params=params
    )

    testObj.snapshot("INIT")

    ledger = testObj.early_day_tick()
    testObj.snapshot("AFTER OPEN TICK", ledger)

    testObj.day_tick()
    testObj.snapshot("AFTER INTERACTION", testObj.day_ledger)

    testObj.late_day_tick()
    testObj.snapshot("AFTER CLOSE TICK", testObj.day_ledger)
