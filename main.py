from definitions import *
from utils import setLogging


def main():
    # Argument parsing
    setLogging(False)

    # Process data
    f_name = "sampleInput/inputOmp.txt"
    d = ExperimentCollection.from_txt_file(f_name)
    print(f"Experiment results from file {f_name}")
    d.print_experiments()
    d.print_scal("OMP")
    print("Done")

    # Plot data
    print("Plotting data to a file...")
    d.plot_scalability(in_base="OMP", as_categorical=False, save_name="myPlot")
    d.plot_scalability(in_base="OMP", as_categorical=True, save_name="myPlotAsCategorical")
    print("Done")
    exit(0)


if __name__ == "__main__":
    main()
