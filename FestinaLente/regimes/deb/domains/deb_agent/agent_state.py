


from dataclasses import dataclass

from FestinaLente.regimes.deb.domains.deb_agent.agent_register.agent_flux import SheepFluxes, compute_fluxes
from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon
from FestinaLente.regimes.deb.univers_compiler.agent_compiler import AgentDerived, derive_sheep_taxon



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







def agent_state_init(agent_id, agent_taxon : SheepTaxon, filling_ratio: float) -> SheepAgentState:
    if filling_ratio < 0:
        raise ValueError("filling ratio must be >= 0 ")
    

    
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

    E_reserve = get_reserve_energy_from_volume(
        structural_volume_cm3=V_init,
        reserve_fill_ratio=filling_ratio,
        reserve_capacity_J_per_cm3=derived_values.E_m_J_per_cm3
    )
    





    return SheepAgentState(
        age_d=0,
        agent_id=agent_id,
        E_J=E_reserve,
        V_cm3=V_init,
        E_H_J=maturity_init, 
        E_R_J=0
    )




