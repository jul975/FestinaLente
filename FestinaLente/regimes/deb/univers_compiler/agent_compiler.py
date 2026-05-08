


from dataclasses import dataclass

from FestinaLente.regimes.deb.taxon_registery.sheep import SheepTaxon


@dataclass(frozen=True)
class AgentDerived:
    """
    Species-level derived DEB quantities.

    These values are computed once from SheepTaxon and used by the flux equations.
    """

    k_M_per_d: float
    # 1 / day.
    # Somatic maintenance rate coefficient.
    # Formula: k_M = [p_M] / [E_G]

    maintenance_ratio_k: float
    # dimensionless.
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

    # Male-specific derived values
    p_Am_male_J_per_d_cm2: float
    E_m_male_J_per_cm3: float
    g_male: float
    L_m_male_cm: float
    V_m_male_cm3: float

@dataclass(frozen=True)
class AgentGenetics:
    """ Contains all species level invariables """
    agent_taxon: SheepTaxon
    agent_derived: AgentDerived


def derive_sheep_taxon(taxon: SheepTaxon) -> AgentDerived:
    """
    Compute derived DEB quantities from species-level anchors.
    """

    k_M = taxon.p_M_J_per_d_cm3 / taxon.E_G_J_per_cm3
    maintenance_ratio_k = taxon.k_J_per_d / k_M
    p_Am = taxon.z * taxon.p_M_J_per_d_cm3 / taxon.kappa
    E_m = p_Am / taxon.v_cm_per_d
    g = taxon.E_G_J_per_cm3 / (taxon.kappa * E_m)
    L_m = taxon.v_cm_per_d / (k_M * g)
    V_m = L_m ** 3
    L_T = taxon.p_T_J_per_d_cm2 / taxon.p_M_J_per_d_cm3
    l_T = L_T / L_m if L_m > 0 else 0.0
    L_i = L_m * (taxon.f - l_T)
    V_i = L_i ** 3

    p_Am_male = taxon.z_male * taxon.p_M_J_per_d_cm3 / taxon.kappa
    E_m_male = p_Am_male / taxon.v_cm_per_d
    g_male = taxon.E_G_J_per_cm3 / (taxon.kappa * E_m_male)
    L_m_male = taxon.v_cm_per_d / (k_M * g_male)
    V_m_male = L_m_male ** 3

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
        V_i_cm3=V_i,
        p_Am_male_J_per_d_cm2=p_Am_male,
        E_m_male_J_per_cm3=E_m_male,
        g_male=g_male,
        L_m_male_cm=L_m_male,
        V_m_male_cm3=V_m_male,
    )


