import numpy as np
import matplotlib.pyplot as plt


def plot_results(results, title_suffix=""):
    """
    Plot:
    - Pressure vs Crank Angle
    - Temperature vs Crank Angle
    """

    theta = results["theta_deg"]

    pressure_bar = results["pressure"] / 1e5

    temperature = results["temperature"]

    plt.figure(figsize=(12, 5))

    # =====================================================
    # Pressure
    # =====================================================

    plt.subplot(1, 2, 1)

    plt.plot(
        theta,
        pressure_bar,
        "k",
        linewidth=2
    )

    plt.title("Pressure Trace" + title_suffix)

    plt.xlabel("Crank Angle θ [deg]")

    plt.ylabel("Pressure [bar]")

    plt.grid(True)

    # =====================================================
    # Temperature
    # =====================================================

    plt.subplot(1, 2, 2)

    plt.plot(
        theta,
        temperature,
        "k",
        linewidth=2
    )

    plt.title("Temperature Trace" + title_suffix)

    plt.xlabel("Crank Angle θ [deg]")

    plt.ylabel("Temperature [K]")

    plt.grid(True)

    plt.tight_layout()


def plot_pv(results, title_suffix=""):

    volume = results["volume"]
    pressure_bar = results["pressure"] / 1e5

    plt.figure(figsize=(8, 6))

    plt.plot(
        volume,
        pressure_bar,
        "k",
        linewidth=2
    )

    plt.title("P-V Diagram" + title_suffix)

    plt.xlabel("Volume [m³]")
    plt.ylabel("Pressure [bar]")

    plt.grid(True)
    plt.tight_layout()


def compare_pv(results_list, labels):
    """
    Compare multiple P-V diagrams.

    Useful for:
    - different fuels
    - different spark timings
    - different compression ratios
    """

    plt.figure(figsize=(8, 6))

    for results, label in zip(results_list, labels):

        volume = results["volume"]

        pressure_bar = (
            results["pressure"] / 1e5
        )

        volume_closed = np.append(
            volume,
            volume[0]
        )

        pressure_closed = np.append(
            pressure_bar,
            pressure_bar[0]
        )

        plt.plot(
            volume_closed,
            pressure_closed,
            linewidth=2,
            label=label
        )

    plt.title("P-V Comparison")

    plt.xlabel("Volume [m³]")

    plt.ylabel("Pressure [bar]")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()


def compare_pressure(results_list, labels):
    """
    Compare pressure traces.
    """

    plt.figure(figsize=(8, 6))

    for results, label in zip(results_list, labels):

        theta = results["theta_deg"]

        pressure_bar = (
            results["pressure"] / 1e5
        )

        plt.plot(
            theta,
            pressure_bar,
            linewidth=2,
            label=label
        )

    plt.title("Pressure Comparison")

    plt.xlabel("Crank Angle θ [deg]")

    plt.ylabel("Pressure [bar]")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()


def compare_temperature(results_list, labels):
    """
    Compare temperature traces.
    """

    plt.figure(figsize=(8, 6))

    for results, label in zip(results_list, labels):

        theta = results["theta_deg"]

        temperature = results["temperature"]

        plt.plot(
            theta,
            temperature,
            linewidth=2,
            label=label
        )

    plt.title("Temperature Comparison")

    plt.xlabel("Crank Angle θ [deg]")

    plt.ylabel("Temperature [K]")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()