from dataclasses import dataclass


@dataclass(frozen=True)
class SheepInteractionResult:
    interaction_substeps: int

    movement_cost_due_J: float
    movement_cost_paid_J: float
    movement_deficit_J: float

    soma_budget_start_J: float
    soma_budget_spent_J: float
    remaining_soma_budget_J: float

    harvested_resource_kg_DM: float
    harvested_gross_energy_J: float

    final_x: int
    final_y: int


def interaction_tick():
    # draw rng for harvest success
    # agent_harvests_resource()

    # draw rng for movement success
    # agent_moves()

    return 