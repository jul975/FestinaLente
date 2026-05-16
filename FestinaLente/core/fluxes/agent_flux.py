


from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


@dataclass(frozen=True)
class AgentFluxes:
    """
    Tick-level energy fluxes.

    Convention:
    - fields ending in _per_d are powers/rates.
    - fields ending in _J are amounts over the current tick.
    """

    dt_d: float

    L_cm: float
    # cm.
    # Formula: L = max(V, V_min)^(1/3)

    body_mass_kg: float
    # kg.
    # Approx wet mass used for movement.

    p_C_J_per_d: float
    # J / day.
    # Formula: p_C = E * v / L

    mobilized_J: float
    # J.
    # Formula: M = min(E, p_C * dt)

    soma_budget_J: float
    # J.
    # Formula: B_S = kappa * mobilized_J

    maturity_repro_budget_J: float
    # J.
    # Formula: B_H = (1 - kappa) * mobilized_J

    assimilation_J: float
    # J.
    # Formula scaffold: A = kap_X * harvested_food_energy_J




def compute_fluxes(
    state: SheepAgentState,
    taxon: SheepTaxon,
    assimilation_J: float,
    dt_d: float,
) -> AgentFluxes:
    V_safe = max(state.V_cm3, taxon.V_min_cm3)
    L_cm = V_safe ** (1.0 / 3.0)

    body_mass_kg = max(
        V_safe / 1000.0,
        taxon.min_body_mass_kg,
    )

    p_C = max(state.E_J * taxon.v_cm_per_d / L_cm, 0.0)
    mobilized_J = min(state.E_J, p_C * dt_d)
    soma_budget_J = taxon.kappa * mobilized_J
    maturity_repro_budget_J = (1.0 - taxon.kappa) * mobilized_J

    return AgentFluxes(
        dt_d=dt_d,
        L_cm=L_cm,
        body_mass_kg=body_mass_kg,
        p_C_J_per_d=p_C,
        mobilized_J=mobilized_J,
        soma_budget_J=soma_budget_J,
        maturity_repro_budget_J=maturity_repro_budget_J,
        assimilation_J=assimilation_J,
    )