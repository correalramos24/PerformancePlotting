from scalability import *
from utils import setLogging
import argparse


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Performance plotting scripts")
    parser.add_argument('-f', required=True, help="Input file")
    parser.add_argument('--plot', required=False, help="Enable plotting", action="store_true")
    parser.add_argument('--save', required=False, default=None, help="Enable and define save file name")
    parser.add_argument('--verbose', required=False, action='store_true', help="Enable verbose mode")
    parser.add_argument('--categorical', required=False, action='store_true', help="Get categorical vars")

    args = parser.parse_args()

    # Set loggin
    setLogging(args.verbose)

    # Process data
    f_name = args.f
    print(f"Reading results from file {f_name}")

    d = ExperimentCollection.from_txt_file(f_name)
    d.print_experiments()
        
    if args.plot:
        print("Computing scalability...")
        d.print_scal("OMP")
        print("Launch the ploting")
        d.plot_scalability(in_base="OMP", as_categorical=args.categorical, save_name=args.save)
    
    print("Done")
    exit(0)


if __name__ == "__main__":
    main()
