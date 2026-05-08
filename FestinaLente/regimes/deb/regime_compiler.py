
from FestinaLente.regimes.deb.univers_compiler.agent_compiler import AgentDerived, AgentGenetics, derive_sheep_taxon
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon
from FestinaLente.regimes.deb.univers_compiler.theta_E import CompiledEnergetics, CompiledWorldEnergetics

def _compile_agent_genetics(agent_taxon: SheepTaxon) -> AgentGenetics:
    '''
    All pre-run computed Agent values
    '''
    agent_derived: AgentDerived = derive_sheep_taxon(agent_taxon)

    return AgentGenetics(
        agent_taxon=agent_taxon,
        agent_derived=agent_derived
    )


def _compile_world_law(theta_W: WorldLawSpec, demand_ref_per_tick: float) -> CompiledWorldEnergetics:
    fertility_norm = generate_patch_field(
        width=theta_W.world_width,
        height=theta_W.world_height,
        correlation=theta_W.patch_correlation,
        contrast=theta_W.patch_contrast,
        floor=theta_W.patch_floor,
    )

    capacity_field = theta_W.capacity_anchor * fertility_norm
    initial_stock_field = theta_W.initial_fill_ratio * capacity_field

    total_inflow = theta_W.world_balance_phi * demand_ref_per_tick

    if theta_W.inflow_mode == "uniform":
        weights = np.full_like(capacity_field, 1.0 / capacity_field.size)
    else:
        raw = fertility_norm.copy()
        weights = raw / raw.sum()

    inflow_field = total_inflow * weights

    return CompiledWorldEnergetics(
        world_width=theta_W.world_width,
        world_height=theta_W.world_height,
        capacity_field=capacity_field,
        initial_stock_field=initial_stock_field,
        inflow_field=inflow_field,
    )



def compile_engine_regime():
    agent_genetics: AgentGenetics = _compile_agent_genetics
    world_params = _compile_world_law
