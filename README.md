# Single-Zone Otto Engine Simulator

A Python implementation of a single-zone spark-ignition (SI) engine model based on Otto-cycle thermodynamics and Wiebe combustion modeling.

The simulator predicts in-cylinder pressure, temperature, work output, indicated mean effective pressure (IMEP), efficiency, combustion phasing metrics, and pressure-volume diagrams for different fuels and ignition timings.

---

## Features

* Slider-crank engine geometry model
* Otto-cycle thermodynamic simulation
* Wiebe heat-release combustion model
* Residual gas fraction convergence
* Multiple fuel support:

  * Gasoline
  * E85
  * Ethanol (E100)
* Indicated work calculation
* IMEP calculation
* Efficiency estimation
* Peak pressure analysis
* CA50 combustion phasing analysis
* Pressure-crank angle diagrams
* Temperature-crank angle diagrams
* Pressure-volume (P-V) diagrams

---

## Project Motivation

This project originated as a MATLAB-based internal combustion engine simulation developed for engine thermodynamics studies and was later reimplemented in Python with improved structure, documentation, and diagnostics.

The objective is to provide a transparent educational and engineering-oriented model for studying spark-ignition engine combustion behavior and cycle performance.

---

## Model Description

The model represents the cylinder as a single thermodynamic zone.

Cylinder pressure is calculated by integrating:

dP/dθ = -γ(P/V)dV/dθ + ((γ−1)/V)dQ/dθ

where:

* P = cylinder pressure
* V = cylinder volume
* γ = ratio of specific heats
* Q = released heat
* θ = crank angle

Combustion is modeled using a Wiebe function formulation.

The model currently simulates:

1. Compression
2. Combustion
3. Expansion

Residual gas fraction is estimated iteratively through convergence of cycle parameters.

---

## Supported Fuels

| Fuel     | Description                |
| -------- | -------------------------- |
| Gasoline | Reference fuel             |
| E85      | 85% Ethanol / 15% Gasoline |
| E100     | Pure Ethanol               |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/single-zone-otto-engine.git
cd single-zone-otto-engine
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Simulator

Run:

```bash
python main.py
```

Example inputs:

```text
Intake pressure Pi [bar]: 0.4
Residual gas fraction f [-]: 0.05
Convergence tolerance alpha [-]: 0.005
Ignition timing theta_s [deg]: -20
```

Example fuel selection:

```text
1 - Gasoline
2 - E85
3 - E100
```

---

## Example Results

Typical gasoline simulation results:

```text
IMEP ≈ 5 bar
Efficiency ≈ 41 %
Peak Pressure ≈ 31 bar
Peak Temperature ≈ 2800 K
CA50 ≈ -7°
Peak Pressure Angle ≈ +6°
```

---

## Current Limitations

The current version is intentionally simplified.

Limitations include:

* Single-zone combustion model
* Constant specific heat ratio (γ)
* No heat transfer model
* No knock prediction
* No intake process simulation
* No exhaust process simulation
* No valve timing model

Because gas-exchange processes are not explicitly modeled, the thermodynamic cycle is not fully closed.

---

## Future Development

Planned future improvements:

* Full 720° four-stroke cycle simulation
* Intake and exhaust modeling
* Valve timing events
* Blowdown process
* Variable specific heats
* Heat-transfer correlations
* Multi-zone combustion modeling

---

## Repository Structure

```text
single-zone-otto-engine/

├── main.py
├── calculations.py
├── fuels.py
├── plotting.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Author

Fotios Angelakis

Mechanical Engineer
