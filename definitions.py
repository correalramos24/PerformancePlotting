from typing import List

class Experiment():
    def __init__(self,  time: float=None,timeUnit: str="s",
                        throughput:float=None, throughputUnit:str="performance",
                        name:str=None, extraConfiguration:dict=None) -> None:

        self.name=name
        self.extraConfiguration=extraConfiguration

        if time is None and throughput is None:
            raise Exception("You must provide either time or throught results")

        if throughput is None:
            self.throughputUnit = f"1/{timeUnit}"
            self.throughput = 1 / time
        else:
            self.throughput=throughput
            self.throughputUnit=throughputUnit

        if name is None and extraConfiguration is not None:
            print("INFO: name not defined, using first config...", end=" ")
            fstKey = list(extraConfiguration.keys())[0]
            fstVal = extraConfiguration[fstKey]
            print(f"set name {fstVal}_{fstKey}")
            self.name = f"{fstVal}_{fstKey}"

    def getConfigByKey(self, key):
        return self.extraConfiguration[key]

    def getExperimentResults(self): return self.throughputs

    def getExperimentUnits(self): return self.throughputUnit

    def __repr__(self) -> str:
        ret = f"{self.name} -> {self.throughput} ({self.throughputUnit})"
        return ret
    

class ExperimentCollection():
    
    def __init__(self) -> None:
        self.results : List(Experiment) = []

    def addExperiment(self, e: Experiment):
        self.results.append(e)

    def computeScalability(self, inBase):
        minVal=None
        for e in self.results:
            e.getConfigB

    def computeEff(self):
        pass

    def printExperiments(self):
        list(map(lambda e : print(repr(e)), self.results))