# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:19:53 2026

@author: AKS
"""

"""
Fuel definitions for Otto cycle engine model.

These values come directly from the MATLAB implementation.
"""

from dataclasses import dataclass


@dataclass
class Fuel:
    name: str
    qc: float        # kJ/kg (heating value)
    MBf: float       # kg/kmol (molecular weight fuel)
    Fs: float        # stoichiometric fuel/air ratio
    a_st: float      # stoichiometric air requirement


# ==========================================================
# Base fuel (Gasoline)
# ==========================================================

GASOLINE = Fuel(
    name="Gasoline",
    qc=44510,
    MBf=101.21,
    Fs=0.0655,
    a_st=11.25
)


# ==========================================================
# E85 blend
# ==========================================================

E85 = Fuel(
    name="E85",
    qc=0.85 * 26820 + 0.15 * 44510,
    MBf=0.85 * 46.07 + 0.15 * 101.21,
    Fs=0.85 * 0.1118 + 0.15 * 0.0655,
    a_st=0.85 * 3 + 0.15 * 11.25
)


# ==========================================================
# E100 ethanol
# ==========================================================

E100 = Fuel(
    name="E100",
    qc=26820,
    MBf=46.07,
    Fs=0.1118,
    a_st=3
)


# ==========================================================
# Helper dictionary (optional convenience)
# ==========================================================

FUELS = {
    "gasoline": GASOLINE,
    "e85": E85,
    "e100": E100
}