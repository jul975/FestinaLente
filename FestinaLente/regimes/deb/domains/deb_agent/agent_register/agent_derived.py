"""
should be blueprint for agent logic and top level specs, => DMI RATIOS ETC spec seperately from agent registry entry, which is more for compiled spec and agent class to use.

"""


# birth size
# adult size
# weaning timing
# puberty timing
# maintenance cost
# maturity maintenance rate
# allocation fraction
# growth efficiency
# reproductive efficiency


# daily max intake as fraction of body mass, from DMI data for sheep
from dataclasses import dataclass
from ssl import create_default_context
from tkinter import W

from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon



DMI_RATIOS: dict[str, float] = {
    "newborn": 0.00,   # if milk-fed / not grazing yet
    "juvenile": 0.04,  # growing lamb, post-weaning
    "adult": 0.025,    # maintenance adult on pasture
}

grass_energy_density_J_per_kg_DM = 18_000_000.0


@dataclass(frozen=True)
class AgentDerived:
    """
    Species-level derived DEB quantities.

    These values are computed once from SheepTaxon and used by the flux equations.

    Attributes: 
    - K_M_per_d:
        FORMULA: k_M = [p_M] / [E_G] 
        SOMATIC MAINTENCE RATE COEFFICIENT
            how fast somatic mainanence consumes E rel to building cost
            Km = 0.002 

    - p_Am_J_per_d_cm2: 
        surface area specific max assimilation flux {}
        P_AM = z * P_m/ kappa
    
    - E_m_J_per_cm3: float
        # J / cm^3.
        # Reserve capacity => Stock density parameter 
        => max reserve of storable energy per cm^2
            given how fast E can enter the through surfacivle area 
            and how fast reserves conduct through the organism what 
            reserve density does the organism support 
        # Formula: E_m = p_Am / v


    


    


    """

    k_M_per_d: float
    # 1 / day.
    # Somatic maintenance rate coefficient.
    # Formula: k_M = [p_M] / [E_G]

    maintenance_ratio_k: float
    # dimensionless.
    # Ration of rate coeficients!!!
    # Formula: k = k_J / k_M

    p_Am_J_per_d_cm2: float
    # J / day / cm^2.
    # Surface-area-specific maximum assimilation flux.
    # For female: p_Am = z * p_M / kappa

    E_m_J_per_cm3: float
    # J / cm^3.
    # Reserve capacity.
    # Formula: E_m = p_Am / v

    g: float
    # dimensionless.
    # Energy investment ratio.
    # Formula: g = E_G / (kappa * E_m)

    L_m_cm: float
    # cm.
    # Maximum structural length.
    # Formula: L_m = v / (k_M * g)
    # Equivalent for p_T = 0: L_m = z

    V_m_cm3: float
    # cm^3.
    # Maximum structural volume.
    # Formula: V_m = L_m^3

    L_T_cm: float
    # cm.
    # Heating/surface-maintenance length correction.
    # Formula: L_T = p_T / p_M
    # Ovis p_T = 0, so L_T = 0.

    l_T: float
    # dimensionless.
    # Scaled heating length.
    # Formula: l_T = L_T / L_m

    L_i_cm: float
    # cm.
    # Ultimate structural length at f.
    # Formula: L_i = L_m * (f - l_T)

    V_i_cm3: float
    # cm^3.
    # Ultimate structural volume.
    # Formula: V_i = L_i^3

    # # Male-specific derived values
    # p_Am_male_J_per_d_cm2: float
    # E_m_male_J_per_cm3: float
    # g_male: float
    # L_m_male_cm: float
    # V_m_male_cm3: float

#######################################################################
@dataclass(frozen=True)
class SheepFluxes:
    """
    Tick-level energy fluxes.

    Convention:
    - fields ending in _per_d are powers/rates.
    - fields ending in _J are amounts over the current tick.
    """

    dt_d: float

    L_cm: float
    # cm.
    # Formula: L = max(V, V_min)^(1/3)

    body_mass_kg: float
    # kg.
    # Approx wet mass used for movement.

    p_C_J_per_d: float
    # J / day.
    # Formula: p_C = E * v / L

    mobilized_J: float
    # J.
    # Formula: M = min(E, p_C * dt)

    soma_budget_J: float
    # J.
    # Formula: B_S = kappa * mobilized_J

    maturity_repro_budget_J: float
    # J.
    # Formula: B_H = (1 - kappa) * mobilized_J

    assimilation_J: float
    # J.
    # Formula scaffold: A = kap_X * harvested_food_energy_J

###################################

@dataclass
class SheepAgentState:
    """
    Individual sheep DEB state.

    These values change during simulation.
    """

    agent_id: float

    age_d: float

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


###################################
def compute_fluxes(
    state: SheepAgentState,
    taxon: SheepTaxon,
    assimilation_J: float,
    dt_d: float,
) -> SheepFluxes:
    V_safe = max(state.V_cm3, taxon.V_min_cm3)
    L_cm = V_safe ** (1.0 / 3.0)

    body_mass_kg = max(
        V_safe / 1000.0,
        taxon.min_body_mass_kg,
    )

    p_C = max(state.E_J * taxon.v_cm_per_d / L_cm, 0.0)
    mobilized_J = min(state.E_J, p_C * dt_d)
    soma_budget_J = taxon.kappa * mobilized_J
    maturity_repro_budget_J = (1.0 - taxon.kappa) * mobilized_J

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

@dataclass(frozen=True)
class SheepMaintenanceCosts:
    """
    Tick-level maintenance accounting.

    Maintenance has priority over growth and maturation.
    """


    somatic_maintenance_due_J: float
    # Formula: C_S = [p_M] * V * dt

    somatic_maintenance_paid_J: float
    # Formula: min(B_S, C_S)

    somatic_deficit_J: float
    # Formula: max(C_S - B_S, 0)

    soma_surplus_after_maintenance_J: float
    # Formula: max(B_S - C_S, 0)
    


    maturity_maintenance_due_J: float
    # Formula: C_J = k_J * E_H * dt

    maturity_maintenance_paid_J: float
    # Formula: min(B_H, C_J)

    maturity_deficit_J: float
    # Formula: max(C_J - B_H, 0)

    maturity_surplus_after_maintenance_J: float
    # Formula: max(B_H - C_J, 0)



def derive_sheep_taxon(taxon: SheepTaxon) -> AgentDerived:
    """
    Compute derived DEB quantities from species-level anchors.
    """

    k_M: float = taxon.p_M_J_per_d_cm3 / taxon.E_G_J_per_cm3
    maintenance_ratio_k: float = taxon.k_J_per_d / k_M
    p_Am: float = taxon.z * taxon.p_M_J_per_d_cm3 / taxon.kappa
    E_m: float = p_Am / taxon.v_cm_per_d

    g: float = taxon.E_G_J_per_cm3 / (taxon.kappa * E_m)
    
    L_m: float = taxon.v_cm_per_d / (k_M * g)
    V_m: float = L_m ** 3
    
    L_T: float = taxon.p_T_J_per_d_cm2 / taxon.p_M_J_per_d_cm3
    l_T: float = L_T / L_m if L_m > 0 else 0.0
    
    L_i: float = L_m * (taxon.f - l_T)
    V_i: float = L_i ** 3

    # p_Am_male: float = taxon.z_male * taxon.p_M_J_per_d_cm3 / taxon.kappa
    # E_m_male: float = p_Am_male / taxon.v_cm_per_d
    # g_male: float = taxon.E_G_J_per_cm3 / (taxon.kappa * E_m_male)
    # L_m_male: float = taxon.v_cm_per_d / (k_M * g_male)
    # V_m_male: float = L_m_male ** 3

    return AgentDerived(
        
        k_M_per_d=k_M,
        maintenance_ratio_k=maintenance_ratio_k,
        p_Am_J_per_d_cm2=p_Am,
        E_m_J_per_cm3=E_m,
        
        g=g,
        
        L_m_cm=L_m,
        V_m_cm3=V_m,
        
        L_T_cm=L_T,
        l_T=l_T,

        L_i_cm=L_i,
        V_i_cm3=V_i
    )

def agent_init(agent_taxon : SheepTaxon):

    
    derived_values: AgentDerived = derive_sheep_taxon(agent_taxon)


    def get_wet_mass_size_multiplier(
        ultimate_wet_mass_g: float,
        ultimate_structural_volume_cm3: float,
    ) -> float:
        """
        Empirical wet-mass-to-DEB-structure conversion.

        This is NOT the pure DEB reserve coefficient w.
        It is a size-mapping coefficient:
            wet_mass_g / structural_volume_cm3
        """
        if ultimate_wet_mass_g <= 0:
            raise ValueError("ultimate_wet_mass_g must be > 0")
        if ultimate_structural_volume_cm3 <= 0:
            raise ValueError("ultimate_structural_volume_cm3 must be > 0")

        return ultimate_wet_mass_g / ultimate_structural_volume_cm3


    def get_structural_volume_from_wet_mass_stage1(
        wet_mass_g: float,
        wet_mass_size_multiplier: float,
    ) -> float:
        """
        Stage-1 size proxy.

        Wet mass determines current structural volume.
        Reserve fill ratio does not modify structure yet.
        """
        if wet_mass_g <= 0:
            raise ValueError("wet_mass_g must be > 0")
        if wet_mass_size_multiplier <= 0:
            raise ValueError("wet_mass_size_multiplier must be > 0")

        return wet_mass_g / wet_mass_size_multiplier


    def get_reserve_energy_from_volume(
        structural_volume_cm3: float,
        reserve_fill_ratio: float,
        reserve_capacity_J_per_cm3: float,
    ) -> float:
        """
        E_reserve = e_init * [E_m] * V
        """
        if structural_volume_cm3 <= 0:
            raise ValueError("structural_volume_cm3 must be > 0")
        if not 0.0 <= reserve_fill_ratio <= 1.0:
            raise ValueError("reserve_fill_ratio must be between 0 and 1")
        if reserve_capacity_J_per_cm3 <= 0:
            raise ValueError("reserve_capacity_J_per_cm3 must be > 0")

        return reserve_fill_ratio * reserve_capacity_J_per_cm3 * structural_volume_cm3


    def get_somatic_maintenance_daily_J(
        structural_volume_cm3: float,
        p_M_J_per_d_cm3: float,
    ) -> float:
        """
        C_s = [p_M] * V * dt
        With dt = 1 day.
        """
        if structural_volume_cm3 <= 0:
            raise ValueError("structural_volume_cm3 must be > 0")

        return p_M_J_per_d_cm3 * structural_volume_cm3


    wet_mass_multiplier = get_wet_mass_size_multiplier(
        ultimate_wet_mass_g=agent_taxon.female_ultimate_wet_mass_g,
        ultimate_structural_volume_cm3=derived_values.V_i_cm3,
    )

    V_init = get_structural_volume_from_wet_mass_stage1(
        wet_mass_g=agent_taxon.birth_wet_mass_g,
        wet_mass_size_multiplier=wet_mass_multiplier,
    )

    maturity_init = agent_taxon.E_Hb_J

    def compute_maintence(taxon : SheepTaxon, state : SheepAgentState ,fluxes : SheepFluxes ) -> SheepMaintenanceCosts:
        somatic_maintance = taxon.p_M_J_per_d_cm3 * state.V_cm3
        c_j = taxon.k_J_per_d * state.E_H_J 

        return SheepMaintenanceCosts(
            somatic_maintenance_due_J=somatic_maintance,
            somatic_maintenance_paid_J=min(somatic_maintance, fluxes.soma_budget_J),
            somatic_deficit_J=max(somatic_maintance-fluxes.soma_budget_J, 0),
            soma_surplus_after_maintenance_J=max(fluxes.soma_budget_J - somatic_maintance, 0),

            maturity_maintenance_due_J= c_j,
            maturity_maintenance_paid_J=min(c_j, fluxes.maturity_repro_budget_J),
            maturity_deficit_J=max(c_j-fluxes.maturity_repro_budget_J, 0),
            maturity_surplus_after_maintenance_J=max(fluxes.maturity_repro_budget_J-c_j, 0)



        )

    created_agents: list[type[SheepAgentState]] = []


    for e in [0.01, 0.1, 0.2, 0.5, 1.0]:
        E_reserve = get_reserve_energy_from_volume(
            structural_volume_cm3=V_init,
            reserve_fill_ratio=e,
            reserve_capacity_J_per_cm3=derived_values.E_m_J_per_cm3,
        )



        agent_state = SheepAgentState(
            age_d=0,
            agent_id=e,
            E_J=E_reserve,
            V_cm3=V_init,
            E_H_J=maturity_init, 
            E_R_J=0
        )
        created_agents.append(agent_state)

    for agent in created_agents:

        print()
        print("===============")
        print(f"reserve fill ratio = {agent.agent_id}")
        print(f"structural volume = {agent.V_cm3} cm3")
        print(f"E_reserve = {agent.E_J} J")
        print(f"Maturity = {agent.E_H_J}")

        fluxes: SheepFluxes = compute_fluxes(
            state = agent,
            taxon=agent_taxon,
            assimilation_J= 0, 
            dt_d=1)
        
        print("")
        print("FLUX DATA")
        print(fluxes.dt_d, "dt")
        print(fluxes.L_cm, "L_cm")
        print(fluxes.body_mass_kg, "body_mass")
        print(fluxes.p_C_J_per_d, "pC")
        print(fluxes.mobilized_J, "mobilized_J")
        print(fluxes.soma_budget_J, "soma_budget_j")
        print(fluxes.maturity_repro_budget_J, "maturity_repro_budget_j")
        print(fluxes.assimilation_J, "assimilation")

        maintance_cost: SheepMaintenanceCosts = compute_maintence(taxon=agent_taxon, state=agent, fluxes=fluxes)

        print("")
        print('MAINTEN')
        print(maintance_cost)

        







agent_init(SheepTaxon)