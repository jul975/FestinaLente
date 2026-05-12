from dataclasses import dataclass

@dataclass(frozen=True)
class SheepAssimilationResult:
    harvested_resource_kg_DM: float
    gross_food_energy_J: float
    digestion_efficiency: float
    assimilated_energy_J: float
    feces_loss_J: float