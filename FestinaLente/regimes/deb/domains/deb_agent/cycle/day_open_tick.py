




from FestinaLente.core.fluxes.agent_flux import AgentFluxes, compute_fluxes
from FestinaLente.regimes.deb.domains.deb_agent.derived import AgentDerived
from FestinaLente.regimes.deb.domains.deb_agent.ledger import AgentDayLedger, InteractionBudget, get_interaction_reserve
from FestinaLente.regimes.deb.domains.deb_agent.phases.maintenance import SheepMaintenanceCosts, compute_maintenance
from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


def open_day_tick(
        agent_state:SheepAgentState, 
        derived : AgentDerived, 
        paramsTaxon: SheepTaxon,
        day_length_d: float
        
        ) -> AgentDayLedger:
    """ open day tick: 
        - compute and deduct maintenance costs from reserves,
        - initialize ledger for the new day, 
        - compute max movement distance for the day based on maintenance surplus, 
        -  other pre-interaction computations. 
        
    This is the tick where the agent can decide how much to move 
    based on its reserves and the expected costs of interactions
    
    """

    fluxes: AgentFluxes = compute_fluxes(
        state=agent_state,
        taxon=paramsTaxon,
        assimilation_J=0.0, # assimilation happens during interaction ticks, so 0 for now
        dt_d=day_length_d
    )

    computed_maintenance: SheepMaintenanceCosts = compute_maintenance(
        taxon=paramsTaxon,
        state=agent_state,
        fluxes=fluxes,
        dt=1.0
    )

    interaction_budget: InteractionBudget = get_interaction_reserve(
        maintenance_costs=computed_maintenance,
        delta_t=day_length_d
    )

    return AgentDayLedger(
        agent_id=agent_state.agent_id,
        biological_day=int(agent_state.age_d),
        fluxes=fluxes,
        maintenance_costs=computed_maintenance,
        interaction_budget=interaction_budget
    )