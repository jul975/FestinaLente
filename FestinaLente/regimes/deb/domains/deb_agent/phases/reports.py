
from dataclasses import dataclass


@dataclass(frozen=True)
class DayOpenTickReport:
    biological_day: int
    n_agents_processed: int
    total_mobilized_J: float
    total_somatic_maintenance_due_J: float
    total_somatic_maintenance_paid_J: float
    total_maturity_maintenance_due_J: float
    total_maturity_maintenance_paid_J: float


@dataclass(frozen=True)
class InteractionTickReport:
    biological_day: int
    interaction_index: int
    n_agents_processed: int
    total_distance_m: float
    total_movement_cost_J: float
    total_harvested_DM_kg: float
    total_assimilated_J: float


@dataclass(frozen=True)
class DayCloseTickReport:
    biological_day: int
    n_agents_processed: int
    total_growth_dV_cm3: float
    total_maturity_gain_J: float
    births: int
    deaths: int