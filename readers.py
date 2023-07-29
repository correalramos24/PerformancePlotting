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
        colum_names = None
        with open(self.fName) as f:
            for line_num, line in enumerate(f.readlines()):
                if "#" in line or len(line.split()) == 0:
                    continue  # found comment

                if "$" in line:
                    line = line.replace("$", "")
                    colum_names = line.split()
                    print(f"INFO: Detected {colum_names} fields")
                    if "time" not in colum_names and "throughput" not in colum_names:
                        raise Exception("Time nor throughput set in the column names")
                elif colum_names is not None:
                    data = line.split()
                    if len(data) != len(colum_names):
                        print(f"WARNING: Bad column count at line {line_num}, skipping...")
                        print(data)
                    else:
                        d = {}
                        for i, x, in enumerate(colum_names):
                            d[x] = data[i]
                        e = Experiment(**d)
                    ret.add_experiment(e)
                else:
                    raise f"Unable to find column names in input {self.fName}"
        return ret


class ReadFromCSV(Reader):
    def __init__(self, file_name) -> None:
        super().__init__(file_name)
