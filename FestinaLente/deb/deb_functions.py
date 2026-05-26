

#########################################################



def compute_fluxes(
    state: SheepAgentState,
    taxon: SheepTaxon,
    assimilation_J: float,
    dt_d: float,
) -> SheepFluxes:
    V_safe: float = max(state.V_cm3, taxon.V_min_cm3)
    L_cm = V_safe ** (1.0 / 3.0)

    body_mass_kg: float = max(
        state.body_mass_kg,
        taxon.min_body_mass_kg,
    )

    p_C = max(state.E_J * taxon.v_cm_per_d / L_cm, 0.0)
    mobilized_J: float = min(state.E_J, p_C * dt_d)

    state.E_J -= mobilized_J

    soma_budget_J: float = taxon.kappa * mobilized_J
    maturity_repro_budget_J: float = (1.0 - taxon.kappa) * mobilized_J

    return SheepFluxes(
        dt_d=dt_d,
        L_cm=L_cm,
        body_mass_kg=body_mass_kg,
        p_C_J_per_d=p_C,
        mobilized_J=mobilized_J,
        soma_budget_J=soma_budget_J,
        maturity_repro_budget_J=maturity_repro_budget_J,
        assimilation_J=assimilation_J,
    )


#########################################################
def compute_maintenance(
            taxon : SheepTaxon, 
            state : SheepAgentState ,
            fluxes : SheepFluxes, 
            dt: float = 1.0 
            ) -> SheepMaintenanceCosts:
        
        somatic_maintenance: float = taxon.p_M_J_per_d_cm3 * state.V_cm3 * dt
        c_j: float = taxon.k_J_per_d * state.E_H_J *dt

        return SheepMaintenanceCosts(
            somatic_maintenance_due_J=somatic_maintenance,
            somatic_maintenance_paid_J=min(somatic_maintenance, fluxes.soma_budget_J),
            somatic_deficit_J=max(somatic_maintenance-fluxes.soma_budget_J, 0),
            soma_surplus_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintenance, 0),

            maturity_maintenance_due_J= c_j,
            maturity_maintenance_paid_J=min(c_j, fluxes.maturity_repro_budget_J),
            maturity_deficit_J=max(c_j-fluxes.maturity_repro_budget_J, 0),
            maturity_surplus_after_maintenance_J=max(fluxes.maturity_repro_budget_J-c_j, 0)



        )


#########################################################


def compute_growth(
    remaining_J: float,
    state_V_cm3: float, 
    taxon_E_G_J_per_cm3: float
    ) -> SheepGrowthResult:

    soma_surplus_after_movement_J: float = remaining_J
    growth_energy_J: float = max(soma_surplus_after_movement_J, 0)

    dV_cm3: float = growth_energy_J / taxon_E_G_J_per_cm3

    V_next_cm3: float = state_V_cm3 + dV_cm3

    return SheepGrowthResult(
        growth_energy_J=growth_energy_J,
        dV_cm3=dV_cm3,
        V_next_cm3=V_next_cm3
    )




#########################################################



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

#########################################################



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


#########################################################
