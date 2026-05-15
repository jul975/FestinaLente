




from FestinaLente.core.fluxes.agent_flux import AgentFluxes, compute_fluxes
from FestinaLente.regimes.deb.domains.deb_agent.derived import AgentDerived
from FestinaLente.regimes.deb.domains.deb_agent.ledger import AgentDayLedger, InteractionBudget, get_interaction_reserve
from FestinaLente.regimes.deb.domains.deb_agent.phases.flux import SheepFluxes
from FestinaLente.regimes.deb.domains.deb_agent.phases.maintenance import SheepMaintenanceCosts
from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon





#########################################################

def compute_fluxes(
    state: SheepAgentState,
    taxon: SheepTaxon,
    assimilation_J: float,
    dt_d: float,
) -> SheepFluxes:
    V_safe: float = max(state.V_cm3, taxon.V_min_cm3)
    L_cm = V_safe ** (1.0 / 3.0)

    body_mass_kg: float = max(
        state.body_mass_kg,
        taxon.min_body_mass_kg,
    )

    p_C = max(state.E_J * taxon.v_cm_per_d / L_cm, 0.0)
    mobilized_J: float = min(state.E_J, p_C * dt_d)

    state.E_J -= mobilized_J

    soma_budget_J: float = taxon.kappa * mobilized_J
    maturity_repro_budget_J: float = (1.0 - taxon.kappa) * mobilized_J

    return SheepFluxes(
        dt_d=dt_d,
        L_cm=L_cm,
        body_mass_kg=body_mass_kg,
        p_C_J_per_d=p_C,
        mobilized_J=mobilized_J,
        soma_budget_J=soma_budget_J,
        maturity_repro_budget_J=maturity_repro_budget_J,
        assimilation_J=assimilation_J,
    )


#########################################################
def compute_maintenance(
            taxon : SheepTaxon, 
            state : SheepAgentState ,
            fluxes : SheepFluxes, 
            dt: float = 1.0 
            ) -> SheepMaintenanceCosts:
        
        somatic_maintenance: float = taxon.p_M_J_per_d_cm3 * state.V_cm3 * dt
        c_j: float = taxon.k_J_per_d * state.E_H_J *dt

        return SheepMaintenanceCosts(
            somatic_maintenance_due_J=somatic_maintenance,
            somatic_maintenance_paid_J=min(somatic_maintenance, fluxes.soma_budget_J),
            somatic_deficit_J=max(somatic_maintenance-fluxes.soma_budget_J, 0),
            soma_surplus_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintenance, 0),

            maturity_maintenance_due_J= c_j,
            maturity_maintenance_paid_J=min(c_j, fluxes.maturity_repro_budget_J),
            maturity_deficit_J=max(c_j-fluxes.maturity_repro_budget_J, 0),
            maturity_surplus_after_maintenance_J=max(fluxes.maturity_repro_budget_J-c_j, 0)



        )



#########################################################
#########################################################
#########################################################
#########################################################
#########################################################
#########################################################



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

    
    return AgentDayLedger(
        agent_id=agent_state.agent_id,
        biological_day=int(agent_state.age_d),
        fluxes=fluxes,
        soma_after_maintenance_J=computed_maintenance.soma_surplus_after_maintenance_J,
        maturity_after_maintenance_J=computed_maintenance.maturity_surplus_after_maintenance_J,
        interaction_ticks_total=0, # to be updated during interaction ticks
        interaction_ticks_completed=0,
        movement_budget_per_tick_J=computed_maintenance.soma_surplus_after_maintenance_J, # for now, all maintenance surplus goes to movement budget, but this can be adjusted based on expected interaction costs
        movement_budget_per_tick_m=computed_maintenance.soma_surplus_after_maintenance_J / paramsTaxon.movement_cost_J_per_m if computed_maintenance.soma_surplus_after_maintenance_J > 0 else 0.0

    )