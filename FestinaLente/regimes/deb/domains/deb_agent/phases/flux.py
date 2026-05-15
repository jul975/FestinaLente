from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.state import SheepAgentState
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


@dataclass(frozen=True)
class SheepFluxes:
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


###################################
