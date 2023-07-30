from typing import List
import matplotlib.pyplot as plt
from utils import log


class Experiment:
    def __init__(self, throughput=None, throughput_unit: str = "throughput",
                 time=None, time_unit: str = "s", name: str = None, **params) -> None:

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
            fst_key = list(params.keys())[0]
            fst_val = params[fst_key]
            log[0](f'Name not defined, using the first configuration as name: {fst_val}_{fst_key}\n')
            self.name = f"{fst_val}_{fst_key}"

    def get_exp_parameter(self, key):
        return self.params[key]

    def add_exp_parameter(self, key, value):
        self.params[key] = value

    def has_exp_parameter(self, key):
        return key in self.params.keys()

    def get_exp_result(self):
        return self.throughput

    def get_exp_result_unit(self):
        return self.throughputUnit

    def get_params_names(self):
        ret = "Name throughput (throughputUnit) Params:"
        for k in self.params.keys():
            ret += f" {k}"
        return ret

    def __repr__(self) -> str:
        ret = f"{self.name} {self.throughput} ({self.throughputUnit}) Params: "
        for k in self.params.values():
            ret += f"{k} "
        return ret


class ExperimentCollection:

    def __init__(self, experiments: List[Experiment] = None, file_name: str = None) -> None:
        if experiments is None:
            experiments = []
        self.scal_config: str = ""
        self.results: List[Experiment] = experiments
        self.file_name = file_name

    @classmethod
    def from_txt_file(cls, file_name):
        aux_exp = []
        with open(file_name) as f:
            colum_names = []
            for line_num, line in enumerate(f.readlines()):
                if "#" in line or len(line.split()) == 0:
                    continue  # found comment

                if "$" in line:
                    line = line.replace("$", "")
                    colum_names = line.split()
                    log[0](f"Detected {colum_names} fields at file {file_name}\n")
                    if "time" not in colum_names and "throughput" not in colum_names:
                        raise Exception("Time nor throughput set in the column names")
                elif colum_names is not None:
                    data = line.split()
                    if len(data) != len(colum_names):
                        log[1](f"WARNING: Bad column count at line {line_num}, skipping...\n")
                        print(data)
                    else:
                        d = {}
                        for i, x, in enumerate(colum_names):
                            d[x] = data[i]
                        aux_exp.append(Experiment(**d))
                else:
                    raise f"Unable to find column names in input {file_name}"

        return cls(aux_exp, file_name)

    def add_experiment(self, e: Experiment):
        self.results.append(e)

    def print_experiments(self):
        print(self.results[0].get_params_names())
        list(map(lambda e: print(repr(e)), self.results))

    def print_scal(self, in_base):
        self.__compute_scalability(in_base)
        self.results.sort(key=lambda ex: ex.get_exp_parameter(in_base))
        print(f"{in_base} Expected Sp(X) Real Sp(X)")
        for x in self.results:
            print(x)

    def plot_scalability(self, in_base, as_categorical=False, save_name=None):
        self.__compute_scalability(in_base)

        self.results.sort(key=lambda ex: ex.get_exp_parameter(in_base))

        cfg, real, expected = [], [], []
        for exp in self.results:
            cfg.append(exp.get_exp_parameter(in_base))
            real.append(exp.get_exp_parameter(f"expected_scal_by{in_base}"))
            expected.append(exp.get_exp_parameter(f"real_scal_by{in_base}"))

        if not as_categorical:
            cfg = [int(x) for x in cfg]
        plt.figure()
        plt.plot(cfg, real, label="Real Sp(X)")
        plt.plot(cfg, expected, label="Expected Sp(X)")
        plt.ylabel("Speedup (X)")
        plt.xlabel(in_base)
        plt.title(f"Scaling {in_base}")
        plt.legend()
        if save_name is not None:
            log[0](f"Saving plot to {save_name}\n")
            plt.savefig(save_name + ".png")
        else:
            plt.show()

    def __compute_scalability(self, in_base):
        if len(self.results) < 1:
            log[1]("Empty experiments collection, can't compute anything\n")
            return

        if self.results[0].has_exp_parameter(f"expected_scal_by{in_base}"):
            log[0](f"Caching scalability results for {in_base}\n")
            return

        # Get the minimum config of all the experiments:
        min_config_obj = min(self.results, key=lambda exp: exp.get_exp_parameter(in_base))
        min_config = min_config_obj.get_exp_parameter(in_base)
        min_val = min_config_obj.get_exp_result()

        log[0](f"Using {in_base} {min_config} as the reference with result {min_val}.\n")

        for e in self.results:
            e_cfg = e.get_exp_parameter(in_base)
            e.add_exp_parameter(f"expected_scal_by{in_base}", self._expected_sp(min_config, e_cfg))
            e.add_exp_parameter(f"real_scal_by{in_base}", self._real_sp(min_val, e.get_exp_result()))

    def __compute_efficiency(self):
        pass

    @staticmethod
    def _expected_sp(min_config, x_config):
        # expected Sp = x_config / min_config
        return float(x_config) / float(min_config)

    @staticmethod
    def _real_sp(min_result, x_result):
        # real Sp = throughput_min / throughput_x
        return float(x_result) / float(min_result)
