
#########################################################





from FestinaLente.regimes.deb.domains.deb_agent.cycle.day_open_tick import open_day_tick
from FestinaLente.regimes.deb.domains.deb_agent.derived import AgentDerived
from FestinaLente.regimes.deb.domains.deb_agent.ledger import AgentDayLedger
from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState, agent_state_init
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


class TestAgentDay:
    def __init__(self,
                  agent_id: int ,
                  params: SheepTaxon  ) -> None:
        self.params: SheepTaxon = params

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
        self.day_ledger = open_day_tick(self.state, self.params, self.derived)
        return self.day_ledger

    def day_tick(self) -> AgentDayLedger:
        pass

    def late_day_tick(self) -> None:
        pass


    def step(self) -> None:
        ## entry point for day tick-level updates
        pass



        




if __name__ == "__main__":
    params = SheepTaxon()
    testObj = TestAgentDay(
        agent_id=1,
        params=params
    )

    print(testObj.state)



