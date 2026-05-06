from dataclasses import dataclass

import numpy as np

from FestinaLente.core.contracts.step_results import AgentSetup
from FestinaLente.regimes.deb.agent_compiler import AgentGenetics


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




@dataclass
class AgentState:
    """
    Individual sheep DEB state.

    These values change during simulation.
    """

    agent_id: int
    parent_id: int | None
    offspring_count: int

    status: int ## status level/maturity

    position: tuple[int, int]
    age_d: float
    alive: bool

    E_J: float
    # J. Reserve energy.
    # Stored usable reserve.

    V_cm3: float
    # cm^3. Structural volume.
    # Determines length, maintenance, body mass approximation.

    E_H_J: float
    # J. Maturity.
    # Developmental information, not usable reserve.

    E_R_J: float
    # J. Reproduction buffer.
    # Adult surplus from maturity/reproduction branch.



class DEBAgent:
    def __init__(
        self, 
        id : np.int64, 
        agent_setup : AgentSetup, 
        position : tuple[np.int64, np.int64], 
        agent_genetics: AgentGenetics, 
          
    ) -> None:

        self._init_rngs(agent_setup)
        #self._id_setup(id)
        self._state_setup(id, agent_genetics)

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
    
    # _initiate agent function
    # => need id setup
    # => need initial state setup


    def _state_setup(self, creation_id, position ,agent_genetics : AgentGenetics) -> None:
        self.id = creation_id
        self.state = AgentState(
            agent_id=creation_id,
            parent_id=0,
            offspring_count=0,
            position=position,
            age_d=0,
            alive=True,
            E_J=agent_genetics.agent_taxon.
        )
    

    def update_agent_state(): 
        # => call deb kernel 
        pass
