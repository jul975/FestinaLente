"""
Sheep specific values from amp
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SheepTaxon:
    """
    Species-level Ovis aries DEB parameters and simulator extensions.

    Values are copied from the Ovis aries AmP entry / pars_init_Ovis_aries.m,
    except movement fields, which are simulator-level locomotion extensions.
    """

    # -------------------------
    # Identity / model metadata
    # -------------------------
    species_name: str = "Ovis aries"
    common_name: str = "domestic sheep"
    deb_model: str = "stx"

    # -------------------------
    # Temperature anchors
    # -------------------------
    T_ref_K: float = 293.15
    # K. Reference temperature for DEB parameters.
    # Formula use: rates are defined at this temperature.

    T_A_K: float = 8000.0
    # K. Arrhenius temperature.
    # Represents thermal sensitivity of physiological rates.

    T_body_K: float = 273.15 + 38.8
    # K. Typical sheep body temperature from mydata file.

    # -------------------------
    # Feeding / assimilation anchors
    # -------------------------
    z: float = 8.3796
    # dimensionless. Female zoom factor.
    # In AmP/DEB, z scales maximum structural length and assimilation.

    z_male: float = 9.0049
    # dimensionless. Male zoom factor.

    F_m_l_per_d_cm2: float = 6.5
    # l / day / cm^2.
    # Maximum surface-area-specific searching rate.

    kap_X: float = 0.8
    # dimensionless.
    # Digestion efficiency: fraction of food energy converted to reserve.

    kap_P: float = 0.1
    # dimensionless.
    # Faecation efficiency.

    f: float = 1.0
    # dimensionless.
    # Scaled functional response used for zero-variate predictions.

    f_tW: float = 1.117
    # dimensionless.
    # Scaled functional response used for time-weight data fitting.

    # -------------------------
    # Reserve mobilisation / allocation
    # -------------------------
    v_cm_per_d: float = 0.027372
    # cm / day.
    # Energy conductance.
    # Controls reserve mobilisation rate.
    # Formula: p_C = E * v / L in DEB-lite.

    kappa: float = 0.79779
    # dimensionless.
    # Allocation fraction to soma.
    # Formula: B_soma = kappa * M

    kappa_R: float = 0.95
    # dimensionless.
    # Reproduction efficiency.
    # Conversion from reproduction buffer to offspring investment.

    # -------------------------
    # Somatic maintenance / growth
    # -------------------------
    p_M_J_per_d_cm3: float = 2510.8646
    # J / day / cm^3.
    # Volume-specific somatic maintenance.
    # Formula: C_S = p_M * V * dt

    p_T_J_per_d_cm2: float = 0.0
    # J / day / cm^2.
    # Surface-specific somatic maintenance.
    # Ovis has 0 here; ignore in first version.

    E_G_J_per_cm3: float = 7851.4521
    # J / cm^3.
    # Specific cost of structure.
    # Formula: dV = growth_energy_J / E_G

    kappa_G: float = 0.7994
    # dimensionless.
    # Growth efficiency from pseudo-data.
    # Do not multiply by this if E_G already includes overhead.

    # -------------------------
    # Maturity / reproduction thresholds
    # -------------------------
    k_J_per_d: float = 0.002
    # 1 / day.
    # Maturity maintenance rate coefficient.
    # Formula: C_J = k_J * E_H * dt

    E_Hb_J: float = 2.933e6
    # J. Maturity at birth.
    # Functional transition: start of feeding.

    E_Hx_J: float = 3.591e7
    # J. Maturity at weaning.
    # For your simplified model: good threshold for movement-enabled juvenile.

    E_Hp_J: float = 1.580e8
    # J. Female maturity at puberty.
    # Functional transition: maturation stops, reproduction buffer starts.

    E_Hpm_J: float = 1.814e8
    # J. Male maturity at puberty.
    # Ignore unless sex-specific agents are active.

    # -------------------------
    # Aging / mortality
    # -------------------------
    h_a_per_d2: float = 2.587e-15
    # 1 / day^2.
    # Weibull aging acceleration.
    # Later mortality model.

    s_G: float = 0.1
    # dimensionless.
    # Gompertz stress coefficient.
    # Later mortality model.

    # -------------------------
    # Foetal / stx-specific values
    # -------------------------
    t_0_d: float = 32.0
    # day.
    # Time at start of fetal development.

    del_M: float = 0.117
    # dimensionless.
    # Shape coefficient for foetal crown-rump length.

    sF: float = 1.0
    # dimensionless.
    # Slow/fast fetal development parameter.

    # -------------------------
    # Empirical life-history anchors
    # -------------------------
    gestation_d: float = 146.0
    weaning_d: float = 135.0
    female_puberty_d: float = 548.0
    male_puberty_d: float = 914.0
    lifespan_d: float = 22.8 * 365.0

    birth_wet_mass_g: float = 5.4e3
    female_ultimate_wet_mass_g: float = 86e3
    male_ultimate_wet_mass_g: float = 110e3

    max_reproduction_rate_per_d: float = 1.58 / 365.0

    # -------------------------
    # Movement simulator extensions
    # -------------------------
    cell_size_m: float = 25.0
    # m / cell.
    # Spatial scale of one ecological grid cell.

    baseline_daily_path_length_m: float = 9600.0
    # m / day.
    # Daily energetic path length, not net displacement.

    adult_max_path_length_m_per_d: float = 9600.0
    # m / day.
    # Species-level movement ceiling.

    stay_activity_fraction: float = 0.25
    # dimensionless.
    # If action == stay, still allow local grazing activity.

    c_transport_flat_J_per_kg_m: float = 2.35
    # J / kg / m.
    # Flat-terrain base cost of transport.
    # Simulator extension, not an AmP parameter.

    rugged_terrain_factor: float = 1.65
    # dimensionless.
    # Terrain multiplier. 2.35 * 1.65 ≈ 3.88 J/kg/m effective rugged value.

    min_body_mass_kg: float = 0.1
    # kg.
    # Numerical guard.

    V_min_cm3: float = 1e-6
    # cm^3.
    # Numerical guard for structural volume.


    ### temp location source from borckway
    baseline_c_transport_J_per_kg_m: float = 2.35
