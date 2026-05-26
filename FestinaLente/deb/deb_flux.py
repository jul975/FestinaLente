from dataclasses import dataclass

from FestinaLente.empirical_data.sheep import SheepTaxon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from FestinaLente.deb.deb_state import SheepAgentState



@dataclass(frozen=True)
class FluxesLedger:
    """
    Tick-level energy fluxes.

    Convention:
    - fields ending in _per_d are powers/rates.
    - fields ending in _J are amounts over the current tick.
    """

    dt_d: float

    L_cm: float
    body_mass_kg: float

    p_C_J_per_d: float
    mobilized_J: float
    soma_budget_J: float
    maturity_repro_budget_J: float
    assimilation_J: float

    @staticmethod
    def _fmt_J(value: float) -> str:
        """Format energy amounts in readable J/kJ/MJ units."""
        abs_value = abs(value)

        if abs_value >= 1_000_000:
            return f"{value / 1_000_000:.3f} MJ"
        if abs_value >= 1_000:
            return f"{value / 1_000:.3f} kJ"
        return f"{value:.2f} J"

    @staticmethod
    def _fmt_rate_J_per_d(value: float) -> str:
        """Format energy flux rates in readable J/d, kJ/d, or MJ/d."""
        abs_value = abs(value)

        if abs_value >= 1_000_000:
            return f"{value / 1_000_000:.3f} MJ/d"
        if abs_value >= 1_000:
            return f"{value / 1_000:.3f} kJ/d"
        return f"{value:.2f} J/d"

    def __str__(self) -> str:
        return (
            "FluxesLedger\n"
            "------------\n"
            f"dt:                     {self.dt_d:.4f} d\n"
            f"structural length:      {self.L_cm:.3f} cm\n"
            f"body mass:              {self.body_mass_kg:.3f} kg\n"
            "\n"
            "Mobilization\n"
            f"  p_C:                  {self._fmt_rate_J_per_d(self.p_C_J_per_d)}\n"
            f"  mobilized:            {self._fmt_J(self.mobilized_J)}\n"
            "\n"
            "Budget split\n"
            f"  soma budget:          {self._fmt_J(self.soma_budget_J)}\n"
            f"  maturity/repro budget:{self._fmt_J(self.maturity_repro_budget_J)}\n"
            "\n"
            "Assimilation\n"
            f"  assimilated:          {self._fmt_J(self.assimilation_J)}"
        )

###################################


def compute_fluxes(
    state: "SheepAgentState",
    taxon: SheepTaxon,
    assimilation_J: float,
    dt_d: float,
) -> FluxesLedger:
    V_safe = max(state.V_cm3, taxon.V_min_cm3)
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

    return FluxesLedger(
        dt_d=dt_d,
        L_cm=L_cm,
        body_mass_kg=body_mass_kg,
        p_C_J_per_d=p_C,
        mobilized_J=mobilized_J,
        soma_budget_J=soma_budget_J,
        maturity_repro_budget_J=maturity_repro_budget_J,
        assimilation_J=assimilation_J,
    )