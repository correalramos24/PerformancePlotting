from typing import List, Dict


class Experiment:
    def __init__(self, throughput=None, throughput_unit: str = "throughput",
                 time=None, time_unit: str = "s",
                 name: str = None, **params) -> None:

        self.name = name
        self.params = params

        if time is None and throughput is None:
            raise Exception("You must provide either time or throughput results")

        if throughput is None:
            self.throughputUnit = f"1/{time_unit}"
            self.throughput = 1 / float(time)
        else:
            self.throughput = float(throughput)
            self.throughputUnit = throughput_unit

        if name is None and params is not None:
            print("INFO: name not defined, using first config...", end=" ")
            fst_key = list(params.keys())[0]
            fst_val = params[fst_key]
            print(f"set name {fst_val}_{fst_key}")
            self.name = f"{fst_val}_{fst_key}"

    def get_config_by_key(self, key):
        return int(self.params[key])

    def get_experiment_result(self):
        return self.throughput

    def get_experiment_unit(self):
        return self.throughputUnit

    def __repr__(self) -> str:
        ret = f"{self.name} -> {self.throughput} ({self.throughputUnit})"
        return ret


class ExperimentCollection:

    def __init__(self) -> None:
        self.scal_config: str = ""
        self.scal: Dict = {}
        self.results: List[Experiment] = []

    def add_experiment(self, e: Experiment):
        self.results.append(e)

    def compute_scalability(self, in_base) -> {}:
        if len(self.results) < 1:
            print("WARNING: Empty experiments collection, can't compute anything")
            return
        self.scal_config = in_base
        # Get the minimum config of all the experiments:
        min_config = self.results[0].get_config_by_key(in_base)
        min_val = self.results[0].get_experiment_result()
        for e in self.results:
            if min_config > e.get_config_by_key(in_base):
                min_config = e.get_config_by_key(in_base)
                min_val = e.get_experiment_result()

        print(f"INFO: Using {in_base} {min_config} as the reference with result {min_val}.")

        self.scal = {}  # in_base -> (expected, real) scal X
        for e in self.results:
            config = e.get_config_by_key(in_base)
            self.scal[config] = (self._expected_sp(min_config, config),
                                 self._real_sp(min_val, e.get_experiment_result())
                                 )
        return self.scal

    def compute_efficiency(self):
        pass

    def print_experiment(self):
        list(map(lambda e: print(repr(e)), self.results))

    def print_scal(self):
        if self.scal is not None:
            print(f"{self.scal_config} Expected Sp(X) Real Sp(X)")
            for key in self.scal:
                print(key, self.scal[key][0], self.scal[key][1])
        else:
            print("Scalability not set")

    @staticmethod
    def _expected_sp(min_config, x_config):
        # expected Sp = x_config / min_config
        return x_config / min_config

    @staticmethod
    def _real_sp(min_result, x_result):
        # real Sp = throughput_min / throughput_x
        return x_result / min_result
