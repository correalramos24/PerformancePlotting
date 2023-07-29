from definitions import *

class Reader():
    def __init__(self, fName) -> None:
        self.fName=fName
        self.descriptor=None

class ReadFromTxt(Reader):
    def __init__(self, fName) -> None:
        super().__init__(fName)

    def parseFile(self):
        ret = ExperimentCollection()

        with open(self.fName) as f:
            for line in f.readlines():
                if "#" in line: 
                    continue    #found comment

                if "$" in line:
                    continue    #found column names
                
                if len(line.split()) == 2:
                    threads, time= line.split()
                    ret.addExperiment(Experiment(time=float(time), extraConfiguration={"OMP":threads}))
                elif len(line.split()) == 3:
                    name, threads, time = line.split()
                    ret.addExperiment(Experiment(name=name, time=float(time), extraConfiguration={"OMP":threads}))
                
        return ret


class ReadfromCSV(Reader):
    def __init__(self, fName) -> None:
        super().__init__(fName)

