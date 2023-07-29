from typing import List


class Experiment:
    def __init__(self, time: float = None, timeunit: str = "s",
                 throughput: float = None, throughput_unit: str = "performance",
                 name: str = None, extra_configuration: dict = None) -> None:

        self.name = name
        self.extraConfiguration = extra_configuration

        if time is None and throughput is None:
            raise Exception("You must provide either time or throught results")

        if throughput is None:
            self.throughputUnit = f"1/{timeunit}"
            self.throughput = 1 / time
        else:
            self.throughput = throughput
            self.throughputUnit = throughput_unit

        if name is None and extra_configuration is not None:
            print("INFO: name not defined, using first config...", end=" ")
            fst_key = list(extra_configuration.keys())[0]
            fst_val = extra_configuration[fst_key]
            print(f"set name {fst_val}_{fst_key}")
            self.name = f"{fst_val}_{fst_key}"

    def get_config_by_key(self, key):
        return self.extraConfiguration[key]

    def get_experiment_result(self):
        return self.throughput

    def get_experiment_unit(self):
        return self.throughputUnit

    def __repr__(self) -> str:
        ret = f"{self.name} -> {self.throughput} ({self.throughputUnit})"
        return ret


class ExperimentCollection:

    def __init__(self) -> None:
        self.results: List[Experiment] = []

    def add_experiment(self, e: Experiment):
        self.results.append(e)

    def compute_scalability(self, in_base):
        min_val = None
        for e in self.results:
            pass

    def compute_efficiency(self):
        pass

    def print_experiment(self):
        list(map(lambda e: print(repr(e)), self.results))
