from dataclasses import dataclass

import numpy as np

from FestinaLente.core.contracts.step_results import AgentSetup


MOVEMENT : int = 1
REPRODUCTION : int = 2
ENERGY : int = 3


"""
NOTE: 
    on engine, only use hash, to interact with agent collection
    agent id, ech cluster in birth and death id's

    tick budget containing branched energy deviations reset each tick, 

"""


@dataclass(frozen=True)
class AgentCreationID:
    owned_id: int
    parent_id: int


@dataclass(frozen=True)
class AgentDeathID:
    owned_id: int
    perent_id: int
    offspring_count: int
    age: int

    # offspring_index: []
    # cause and other metadata as well?
    cause: str


@dataclass(frozen=True)
class PhysiologySpec:
    """Model concept	AmP anchor
    -> species specific physiological parameters, which are used to compute energy flow and life history events.
    -> v, kap, kap_R, p_M, k_J, E_G, E_Hb, E_Hx, E_Hp"""

    v: float  # cm/day
    kappa: float
    kappa_R: float

    p_M: float  # J/day/cm^3
    E_G: float  # J/cm^3
    k_J: float  # 1/day

    E_Hb: float  # birth threshold
    E_Hx: float  # weaning / movement threshold
    E_Hp: float  # puberty threshold

    reserve_init_fraction: float
    structure_init_volume: float

    # Brokway and boyne locomotion equation
    c_transport_eff_J_per_kg_m = 2.35  # calibrated for ~86 kg adult, flat terrain


class DerivedPhysiologySpec:
    """derived parameters for convenience, to avoid repeated calculations."""

    E_Rb: float  # reproduction buffer at birth, J
    E_Rp: float  # reproduction buffer at puberty, J


@dataclass
class AgentState:
    agent_id: int
    offspring_count: int
    age: float

    reserve_energy: float  # J
    position: tuple[
        int, int
    ]  # (x, y) coordinates => as of now, spatial only on engine level,
    structural_volume: float  # cm^3
    maturity: float  # J
    reproduction_buffer: float  # J
    age_days: int
    alive: bool = True

    # movement cost J in state


@dataclass
class PreMovementResult:
    alive: bool
    movement_cost_j: float




class DEBAgent:
    def __init__(
        self, agent_setup: AgentSetup, initial_state: TaxonAnchor, physiology_params: PhysiologySpec 
    ):

        self._init_rngs(agent_setup)
        self.state: AgentState = initial_state
        self.params: PhysiologySpec = physiology_params

    def _init_rngs(self, agent_setup: AgentSetup) -> None:
        """initializes agent lineage."""

        self.move_rng = np.random.Generator(
            np.random.PCG64(agent_setup.identity_words + (MOVEMENT,))
        )
        self.repro_rng = np.random.Generator(
            np.random.PCG64(agent_setup.identity_words + (REPRODUCTION,))
        )
        self.energy_rng = np.random.Generator(
            np.random.PCG64(agent_setup.identity_words + (ENERGY,))
        )

        return
    

    def update_agent_state(): 
        pass
