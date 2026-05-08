"""
Compiled Engine ready structures defining domain specifications. 

Single source of truth for all internal Engine dynamics and assumptions.
returning structure should be containing all domains and be used for all internal Engine dynamics and assumptions.

"""


from dataclasses import dataclass
import numpy as np

from FestinaLente.regimes.deb.univers_compiler.agent_compiler import AgentGenetics




@dataclass(frozen=True)
class CompiledWorldEnergetics:
    world_width: int
    world_height: int
    capacity_field: np.ndarray
    initial_stock_field: np.ndarray
    inflow_field: np.ndarray



@dataclass(frozen=True)
class CompiledEngineParameters:
    ''' PLACEHOLDER '''
    animal_params: AgentGenetics
    
    world_energetics: CompiledWorldEnergetics