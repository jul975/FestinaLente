
"""
Dataclasses representing current agent/world state
"""
from dataclasses import dataclass


from FestinaLente.empirical_data.sheep import SheepTaxon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    
    from FestinaLente.deb.deb_species import AnimalSpecies



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

    movement_ratio: float
    # adult_max_path_length_m_per_d
    #              X
    # c_transport_flat_J_per_kg_m
    #
    # => constant for each species and given max path length => needs to be made per species and per maturity level for prototype
    


    # # Male-specific derived values
    # p_Am_male_J_per_d_cm2: float
    # E_m_male_J_per_cm3: float
    # g_male: float
    # L_m_male_cm: float
    # V_m_male_cm3: float

    def __str__(self) -> str:
        return (
            f"--- AgentDerived ---\n"
            f"  [Rates]       k_M={self.k_M_per_d:.4f} d⁻¹  |  k={self.maintenance_ratio_k:.6f}  |  p_Am={self.p_Am_J_per_d_cm2:.2e} J/d/cm²\n"
            f"  [Capacity]    E_m={self.E_m_J_per_cm3:.2e} J/cm³  |  g={self.g:.6f}\n"
            f"  [Length]      L_m={self.L_m_cm:.4f} cm  |  L_T={self.L_T_cm:.4f} cm  |  l_T={self.l_T:.4f}  |  L_i={self.L_i_cm:.4f} cm\n"
            f"  [Volume]      V_m={self.V_m_cm3:.4f} cm³  |  V_i={self.V_i_cm3:.4f} cm³\n"
        )

#######################################################################

###################################



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



##############################################################  




@dataclass
class SheepAgentState:
    """
    Individual sheep DEB state.

    These values change during simulation.
    """

    agent_id: float
    # parent_id: float | None = None

    # offspring_count: int = 0


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

    body_mass_kg: float

    wet_weight_init: float

    maturity_status: int = 0
    # 0 = newborn, 1 = juvenile, 2 = adult

    def __str__(self) -> str:
        return (
            f"--- SheepAgentState (id={self.agent_id}, age={self.age_d}d) ---\n"
            f"  [Morphology]  V={self.V_cm3:.2f} cm³  |  body_mass={self.body_mass_kg:.2f} kg\n"
            f"  [Energy]      E={self.E_J:.2e} J  |  E_H={self.E_H_J:.2e} J  |  E_R={self.E_R_J:.2e} J\n"
            f"  [Status]      alive={self.alive}  |  maturity={self.maturity_status}\n"
        )




def agent_state_init(
        agent_id : int, 
        species_obj: "AnimalSpecies", 
        filling_ratio: float, 
        wet_mass_initiator : float|None = None, 
        maturity_status: int = 0
        ) -> SheepAgentState :
    
    if filling_ratio < 0:
        raise ValueError("filling ratio must be >= 0 ")
    
    if wet_mass_initiator == None:
        wet_mass_initiator = species_obj.taxon.birth_wet_mass_g
    
    derived_values: AgentDerived = species_obj.derived


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



    wet_mass_multiplier: float = get_wet_mass_size_multiplier(
        ultimate_wet_mass_g=species_obj.taxon.female_ultimate_wet_mass_g,
        ultimate_structural_volume_cm3=derived_values.V_i_cm3,
    )

    V_init: float = get_structural_volume_from_wet_mass_stage1(
        wet_mass_g=wet_mass_initiator,
        wet_mass_size_multiplier=wet_mass_multiplier,
    )

    maturity_init: float = species_obj.taxon.E_Hb_J

    E_reserve: float = get_reserve_energy_from_volume(
        structural_volume_cm3=V_init,
        reserve_fill_ratio=filling_ratio,
        reserve_capacity_J_per_cm3=derived_values.E_m_J_per_cm3
    )
    


    agent_state = SheepAgentState(
        agent_id=agent_id,
        age_d=0,
        E_J=E_reserve,
        V_cm3=V_init,
        E_H_J=maturity_init,
        E_R_J=0,
        body_mass_kg=wet_mass_initiator/1000,
        wet_weight_init=wet_mass_initiator,
        alive=True,
        maturity_status=maturity_status
    )



    return agent_state





if __name__ == "__main__":
    pass 