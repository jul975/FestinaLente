from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FestinaLente.deb.deb_test.TESTS import AgentTest

@dataclass(frozen=True)
class AgentSnapshotT:
    E_J: float
    V_cm3: float
    E_H_J: float
    age_d: int

    @classmethod
    def from_agent(cls, agent: "AgentTest") -> "AgentSnapshotT":
        return cls(
            E_J=agent.state.E_J,
            V_cm3=agent.state.V_cm3,
            E_H_J=agent.state.E_H_J,
            age_d=agent.age_d,
        )