from definitions import *


class Reader:
    def __init__(self, file_name) -> None:
        self.fName = file_name
        self.descriptor = None


class ReadFromTxt(Reader):
    def __init__(self, file_name) -> None:
        super().__init__(file_name)

    def parse(self):
        ret = ExperimentCollection()

        with open(self.fName) as f:
            for line in f.readlines():
                if "#" in line:
                    continue  # found comment

                if "$" in line:
                    continue  # found column names

                if len(line.split()) == 2:
                    threads, time = line.split()
                    ret.add_experiment(Experiment(time=float(time), extra_configuration={"OMP": threads}))
                elif len(line.split()) == 3:
                    name, threads, time = line.split()
                    ret.add_experiment(Experiment(name=name, time=float(time), extra_configuration={"OMP": threads}))

        return ret


class ReadFromCSV(Reader):
    def __init__(self, file_name) -> None:
        super().__init__(file_name)
