from dataclasses import dataclass
from enum import Enum, auto


class TickKind(Enum):
    DAY_OPEN = auto()
    INTERACTION = auto()
    DAY_CLOSE = auto()


@dataclass(frozen=True)
class DayCycleSpec:
    """
    Defines the repeating engine-level structure of one biological day.

    Example:
        n_interaction_ticks = 4

        DAY_OPEN
        INTERACTION[0]
        INTERACTION[1]
        INTERACTION[2]
        INTERACTION[3]
        DAY_CLOSE
    """

    n_interaction_ticks: int

    def __post_init__(self) -> None:
        if self.n_interaction_ticks <= 0:
            raise ValueError("n_interaction_ticks must be positive.")

    @property
    def ticks_per_day(self) -> int:
        return self.n_interaction_ticks + 2


@dataclass(frozen=True)
class TickToken:
    """
    Fully interpreted engine tick.

    This is passed into cycle handlers so they know where they are
    in the biological day.
    """

    engine_tick: int
    biological_day: int
    index_in_day: int
    kind: TickKind
    interaction_index: int | None = None

    @property
    def is_interaction(self) -> bool:
        return self.kind is TickKind.INTERACTION

    @property
    def is_day_open(self) -> bool:
        return self.kind is TickKind.DAY_OPEN

    @property
    def is_day_close(self) -> bool:
        return self.kind is TickKind.DAY_CLOSE


class SimulationClock:
    """
    Pure interpreter from engine ticks to biological cycle positions.
    """

    def __init__(self, cycle_spec: DayCycleSpec) -> None:
        self.cycle_spec: DayCycleSpec = cycle_spec

    def token_for(self, engine_tick: int) -> TickToken:
        if engine_tick < 0:
            raise ValueError("engine_tick must be non-negative.")

        ticks_per_day = self.cycle_spec.ticks_per_day
        biological_day = engine_tick // ticks_per_day
        index_in_day = engine_tick % ticks_per_day

        if index_in_day == 0:
            return TickToken(
                engine_tick=engine_tick,
                biological_day=biological_day,
                index_in_day=index_in_day,
                kind=TickKind.DAY_OPEN,
            )

        if 1 <= index_in_day <= self.cycle_spec.n_interaction_ticks:
            return TickToken(
                engine_tick=engine_tick,
                biological_day=biological_day,
                index_in_day=index_in_day,
                kind=TickKind.INTERACTION,
                interaction_index=index_in_day - 1,
            )

        return TickToken(
            engine_tick=engine_tick,
            biological_day=biological_day,
            index_in_day=index_in_day,
            kind=TickKind.DAY_CLOSE,
        )