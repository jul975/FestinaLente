"""
external empirical locomotion-cost sources:

"""
from dataclasses import dataclass

@dataclass(frozen=True)
class LocomotionCostSpec:
    """
    c_{transport}​(G,S)=2.35+0.398G+0.0286G^2−0.036S+0.00052S^2
    """
    source: str = "Brockway_Boyne_1980_sheep"
    mode: str = "scalar_fallback"  # or "slope_speed_regression"
    baseline_c_transport_J_per_kg_m: float = 2.35



def brockway_boyne_c_transport(
    gradient_degrees: float,
    speed_m_per_min: float,
) -> float:
    """ NOTE: later implementation """
    return (
        2.35
        + 0.398 * gradient_degrees
        + 0.0286 * gradient_degrees**2
        - 0.036 * speed_m_per_min
        + 0.00052 * speed_m_per_min**2
    )





def compute_locomotion_cost(
    distance_m: float,
    gradient_degrees: float,
    speed_m_per_min: float,
    body_mass_kg: float,
) -> float:
    """ compute locomotion cost in Joules for a given movement """
    c_transport_J_per_kg_m = brockway_boyne_c_transport(
        gradient_degrees=gradient_degrees,
        speed_m_per_min=speed_m_per_min
    )
    return c_transport_J_per_kg_m * body_mass_kg * distance_m


def compute_max_locomotion_distance_m(
    somatic_energy_J: float,
    c_transport_J_per_kg_m: float,
    body_mass_kg: float, 
    terrain_factor: float = 1.0) -> float:
    """ compute maximum locomotion distance in meters given available energy and cost per meter """
    if c_transport_J_per_kg_m <= 0:
        raise ValueError("Transport cost per kg per meter must be positive.")
    if somatic_energy_J <= 0:
        return 0.0  # No energy means no movement
    return somatic_energy_J / (c_transport_J_per_kg_m * body_mass_kg * terrain_factor)