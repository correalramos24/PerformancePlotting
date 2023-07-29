from readers import *
from plotting import *


def main():
    # Argument parsing

    # Process data
    d = ReadFromTxt("sampleInput/inputOmp.txt").parse()

    d.print_experiment()
    # Plot data

    exit(0)


if __name__ == "__main__":
    main()
