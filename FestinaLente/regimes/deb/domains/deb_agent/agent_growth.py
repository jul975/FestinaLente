
from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.agent_interaction_budget import InteractionBudget


@dataclass(frozen=True)
class SheepGrowthResult:
    """
    Structural growth accounting.

    Growth uses soma surplus after maintenance and movement.
    """

    growth_energy_J: float
    # Formula: G = soma_surplus_after_movement

    dV_cm3: float
    # Formula: dV = G / E_G

    V_next_cm3: float
    # Formula: V_next = V + dV



def compute_growth(
    interaction_result: InteractionBudget,
    state_V_cm3: float, 
    taxon_E_G_J_per_cm3: float
    ) -> SheepGrowthResult:

    soma_surplus_after_movement_J: float = interaction_result.somatic_reserve
    growth_energy_J: float = max(soma_surplus_after_movement_J, 0)

    dV_cm3: float = growth_energy_J / taxon_E_G_J_per_cm3

    V_next_cm3: float = state_V_cm3 + dV_cm3

    return SheepGrowthResult(
        growth_energy_J=growth_energy_J,
        dV_cm3=dV_cm3,
        V_next_cm3=V_next_cm3
    )