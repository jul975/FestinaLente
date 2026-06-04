
from dataclasses import dataclass


@dataclass
class SimSetupTest:
    """
    Run specific setup object for engine level params 
    """

    agent_count : int = 1
    bio_day_count: int = 1

    dt_day: int = 4

    start_position_test: tuple = (0.0, 0.0)




def single_agent_test(bio_day_count: int = 1, dt_day: int = 4) -> SimSetupTest:
    """
    positioning == 0,0
    """

    return SimSetupTest(
        bio_day_count=bio_day_count,
        dt_day=dt_day
    )


def multi_agent_test(agent_count: int = 1, bio_day_count: int = 1, dt_day: int = 4) -> SimSetupTest:
    """
    positioning == 0,0
    """

    return SimSetupTest(
        agent_count=agent_count,
        bio_day_count=bio_day_count,
        dt_day=dt_day
    )