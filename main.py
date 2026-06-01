from calculations import run_cycle
from fuels import FUELS
from plotting import plot_results, plot_pv

import matplotlib.pyplot as plt


# ==========================================================
# USER INPUTS
# ==========================================================

def get_inputs():

    print("\n=== Otto Cycle Engine Model ===\n")

    Pi = float(
        input("Intake pressure Pi [bar]: ")
    )

    f = float(
        input("Residual gas fraction f [-]: ")
    )

    alpha = float(
        input("Convergence tolerance alpha [-]: ")
    )

    theta_s = float(
        input("Ignition timing theta_s [deg]: ")
    )

    return Pi, f, alpha, theta_s


# ==========================================================
# FUEL SELECTION
# ==========================================================

def select_fuel():

    print("\nSelect fuel:")
    print("1 - Gasoline")
    print("2 - E85")
    print("3 - E100")

    choice = input("Enter choice: ")

    if choice == "2":
        return FUELS["e85"]

    elif choice == "3":
        return FUELS["e100"]

    else:
        return FUELS["gasoline"]


# ==========================================================
# CONVERGENCE LOOP
# ==========================================================

def convergence_loop(
    Pi,
    f,
    alpha,
    theta_s,
    fuel
):

    max_iter = 100

    for i in range(max_iter):

        result = run_cycle(
            Pi,
            f,
            theta_s,
            fuel
        )

        r1 = result["r1"]
        r2 = result["r2"]

        print(
            f"Iter {i}: "
            f"r1={r1:.6f}, "
            f"r2={r2:.6f}, "
            f"Pi={Pi:.5f}, "
            f"f={f:.5f}"
        )

        if r1 < alpha and r2 < alpha:

            print("\nConverged.\n")

            return result, Pi, f

        # ----------------------------------------------
        # proportional update
        # ----------------------------------------------

        Pi += 0.05 * r1 * Pi

        f += 0.05 * r2 * f

        # ----------------------------------------------
        # safety limits
        # ----------------------------------------------

        Pi = max(Pi, 0.05)

        f = max(f, 0.001)

        f = min(f, 0.20)

    print("\nWARNING: Did not fully converge.")

    return result, Pi, f


# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    Pi, f, alpha, theta_s = get_inputs()

    fuel = select_fuel()

    print(
        f"\nRunning for fuel: "
        f"{fuel.name}\n"
    )

    result, Pi_final, f_final = convergence_loop(
        Pi,
        f,
        alpha,
        theta_s,
        fuel
    )

    # ======================================================
    # RESULTS
    # ======================================================

    print("\n=== RESULTS ===")

    print(
        f"Final Pi: "
        f"{Pi_final:.5f} bar"
    )

    print(
        f"Final f: "
        f"{f_final:.5f}"
    )

    print(
        f"Indicated work: "
        f"{result['work']:.2f} J"
    )

    print(
        f"Indicated power: "
        f"{result['power']:.2f} W"
    )

    print(
        f"IMEP1: "
        f"{result['imep1']/1e5:.3f} bar"
    )

    print(
        f"Efficiency: "
        f"{result['eta']*100:.2f} %"
    )

    # ======================================================
    # EXTRA DIAGNOSTICS
    # ======================================================

    print(
    f"Max pressure: "
    f"{result['pmax']/1e5:.2f} bar"
    )

    print(
    f"Peak pressure angle: "
    f"{result['theta_pmax']:.1f} deg"
    )

    print(
    f"CA50: "
    f"{result['CA50']:.1f} deg"
    )

    print(
        f"Max temperature: "
        f"{max(result['temperature']):.0f} K"
    )

    print(
        f"IMEP1 = "
        f"{result['imep1']/1e5:.3f} bar"
    )

    print(
        f"IMEP2 = "
        f"{result['imep2']/1e5:.3f} bar"
    )

    print(
        f"Initial Pressure = "
        f"{result['pressure'][0]/1e5}"
    )

    print(
        f"Final Pressure = "
        f"{result['pressure'][-1]/1e5}"
    )

    print(
        f"Initial Volume = "
        f"{result['volume'][0]}"
    )

    print(
        f"Final Volume = "
        f"{result['volume'][-1]}"
    )

    # ======================================================
    # CLOSURE ERROR
    # ======================================================

    closure_error = abs(
        1.0
        - result["pressure"][0]
        / result["pressure"][-1]
    )

    print(
        f"Cycle closure error = "
        f"{closure_error*100:.2f}%"
    )

    print(
        f"Initial pressure = "
        f"{result['pressure'][0]/1e5:.3f} bar"
    )

    print(
        f"Final pressure = "
        f"{result['pressure'][-1]/1e5:.3f} bar"
    )

    print(
        f"Tstart = "
        f"{result['temperature'][0]:.1f} K"
    )

    print(
        f"Tend = "
        f"{result['temperature'][-1]:.1f} K"
    )
    
    # ======================================================
    # PLOTS
    # ======================================================

    plot_results(result)

    plot_pv(result)

    plt.show()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()