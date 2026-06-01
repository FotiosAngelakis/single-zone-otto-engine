# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:07:02 2026

@author: AKS
"""

import numpy as np


def run_cycle(
    Pi_bar,
    residual_fraction,
    ignition_deg,
    fuel,
):
    """
    Otto cycle simulation based on the original MATLAB model.

    Parameters
    ----------
    Pi_bar : float
        Intake pressure [bar]

    residual_fraction : float
        Residual gas fraction

    ignition_deg : float
        Spark timing [deg]

    fuel : dict
        Fuel properties

    Returns
    -------
    dict
    """

    # ==========================================================
    # Engine Data
    # ==========================================================

    n_cyl = 4

    rod_length = 0.18      # m

    compression_ratio = 10

    equivalence_ratio = 1.0

    Ti = 313.5             # K

    Pe_bar = 1.1           # bar

    friction_mep_bar = 1.2

    displacement_total_L = 1.5

    rpm = 3000

    bmep_bar = 3

    gamma = 1.4 - (0.16 * equivalence_ratio)

    wiebe_a = 5

    wiebe_n = 2

    combustion_duration_deg = 35

    step_deg = 0.5

    # ==========================================================
    # Fuel Properties
    # ==========================================================

    qc = fuel.qc
    MBf = fuel.MBf
    Fs = fuel.Fs
    a_st = fuel.a_st

    # ==========================================================
    # Gas Constants
    # ==========================================================

    R_universal = 0.082057338

    R_universal *= 101325

    MB_air = 28.97

    # ==========================================================
    # Mixture Properties
    # ==========================================================

    Ysf = 1 / (1 + 4.76 * a_st)

    Ysair = 1 - Ysf

    MB_mix = Ysair * MB_air + Ysf * MBf

    R_spec = R_universal / MB_mix

    rho_i = (Pi_bar * 1e5) / (R_spec * Ti)

    volumetric_eff = (
        1
        - ((Pe_bar / Pi_bar) - 1)
        / (gamma * (compression_ratio - 1))
    )

    Vd = (displacement_total_L / n_cyl) / 1000.0

    m_i = volumetric_eff * rho_i * Vd

    m_air = m_i / (1 + Fs)

    m_fuel = Fs * m_air

    m1 = m_i / (1 - residual_fraction)

    q_in = (
        equivalence_ratio
        * Fs
        * qc
        / (1 + equivalence_ratio * Fs)
    )

    Qin = m_i * q_in * 1000.0

    # ==========================================================
    # Crank Angle Grid
    # ==========================================================

    theta_deg = np.arange(
        -180,
        180 + step_deg,
        step_deg
    )

    theta_rad = np.deg2rad(theta_deg)

    ignition_rad = np.deg2rad(ignition_deg)

    combustion_duration_rad = np.deg2rad(
        combustion_duration_deg
    )

    npts = len(theta_deg)

    # ==========================================================
    # Geometry
    # ==========================================================

    stroke = ((4 * Vd) / np.pi) ** (1 / 3)

    bore = stroke

    Rg = 2 * rod_length / stroke

    # ==========================================================
    # Arrays
    # ==========================================================

    V_theta = np.zeros(npts)

    dVdtheta = np.zeros(npts)

    xb = np.zeros(npts)

    dQdtheta = np.zeros(npts)

    P_theta = np.zeros(npts)

    dPdtheta = np.zeros(npts)

    T_theta = np.zeros(npts)

    DV = np.zeros(npts)

    PDV = np.zeros(npts)

    # ==========================================================
    # Main Loop
    # ==========================================================

    for i in range(npts):

        th = theta_rad[i]

        root_term = np.sqrt(
            max(
                Rg**2 - np.sin(th)**2,
                1e-12
            )
        )

        V_theta[i] = (
            Vd / (compression_ratio - 1)
            + (Vd / 2)
            * (
                Rg
                + 1
                - np.cos(th)
                - root_term
            )
        )

        dVdtheta[i] = (
            (Vd / 2)
            * np.sin(th)
            * (
                1
                + np.cos(th) / root_term
            )
        )

        # ------------------------------------------------------
        # Wiebe Combustion
        # ------------------------------------------------------

        if (
            ignition_deg
            <= theta_deg[i]
            <= ignition_deg + combustion_duration_deg
        ):

            burn_fraction = (
                (
                    theta_deg[i]
                    - ignition_deg
                )
                / combustion_duration_deg
            )

            xb[i] = (
                1
                - np.exp(
                    -wiebe_a
                    * burn_fraction**wiebe_n
                )
            )

            dQdtheta[i] = (
                wiebe_a
                * wiebe_n
                * Qin
                / combustion_duration_rad
                * (1 - xb[i])
                * (
                    (
                        th
                        - ignition_rad
                    )
                    / combustion_duration_rad
                ) ** (wiebe_n - 1)
            )

        # ------------------------------------------------------
        # Pressure Integration
        # ------------------------------------------------------

        if i == 0:

            P_theta[i] = Pi_bar * 1e5

        else:

            P_theta[i] = (
                P_theta[i - 1]
                + dPdtheta[i - 1]
                * np.deg2rad(step_deg)
            )

        dPdtheta[i] = (
            -gamma
            * (P_theta[i] / V_theta[i])
            * dVdtheta[i]
            + (
                (gamma - 1)
                / V_theta[i]
            )
            * dQdtheta[i]
        )

        T_theta[i] = (
            P_theta[i]
            * V_theta[i]
            / (m1 * R_spec)
        )

        if i > 0:

            DV[i] = (
                V_theta[i]
                - V_theta[i - 1]
            )

        PDV[i] = (
            P_theta[i]
            * DV[i]
        )

    # ==========================================================
    # Performance
    # ==========================================================

    W = np.trapz(P_theta, V_theta)

    Wind = n_cyl * W

    pmep = (
        Pe_bar
        - Pi_bar
    ) * 1e5

    amep = (
        2.69
        * (rpm / 1000) ** 1.5
        * 1000
    )

    imep1 = (
        bmep_bar * 1e5
        + friction_mep_bar * 1e5
        + pmep
        + amep
    )

    imep2 = W / Vd

    eta = W / Qin

    eta_net = eta * (
        1
        - (
            bmep_bar * 1e5
            / imep1
        )
    )

    Pind = (
        n_cyl
        * Vd
        * imep1
        * rpm
        / 120
    )

    P4 = P_theta[-1]

    f2 = (
        1 / compression_ratio
    ) * (
        (Pe_bar * 1e5)
        / P4
    ) ** (1 / gamma)

    r1 = abs(
        1
        - imep1 / imep2
    )

    r2 = abs(
        1
        - residual_fraction / f2
    )
# ==========================================================
# Diagnostics
# ==========================================================

    imax = np.argmax(P_theta)

    pmax = P_theta[imax]

    theta_pmax = theta_deg[imax]

    # CA50 (50% mass fraction burned)

    if np.max(xb) > 0.5:

        idx50 = np.argmin(
            np.abs(xb - 0.5)
            )

        CA50 = theta_deg[idx50]

    else:

            CA50 = np.nan
    return {
    "theta_deg": theta_deg,
    "theta_rad": theta_rad,

    "pressure": P_theta,
    "temperature": T_theta,
    "volume": V_theta,

    "burn_fraction": xb,

    "pmax": pmax,
    "theta_pmax": theta_pmax,
    "CA50": CA50,

    "work": W,
    "work_engine": Wind,

    "imep1": imep1,
    "imep2": imep2,

    "eta": eta,
    "eta_net": eta_net,

    "power": Pind,

    "f2": f2,

    "r1": r1,
    "r2": r2,

    "Qin": Qin,

    "m_air": m_air,
    "m_fuel": m_fuel,
}