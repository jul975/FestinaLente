"""
Engine-tick orchestration of agent's daily cycle, including maintenance, interaction, and movement phases.

DAY_OPEN tick:
    for all living agents:
        compute daily mobilization
        deduct from reserve
        compute soma/maturity branches
        pay maintenance
        create AgentDayLedger
        compute movement_budget_per_tick = soma_surplus / n_interaction_ticks

INTERACTION tick k:
    for all living agents:
        compute movement intent capped by movement_budget_per_tick
    resolve all movement
    update positions
    rebuild spatial index
    resolve harvesting/assimilation for this interaction tick
    update ledgers

DAY_CLOSE tick:
    for all living agents:
        apply accumulated assimilation to reserve
        apply remaining soma surplus to growth
        apply maturity/reproduction branch
        handle starvation/death/reproduction if relevant
        increment biological age if appropriate
    clear AgentDayLedger




"""