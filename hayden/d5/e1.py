from queue import LifoQueue
import re

def main():
    with open(file="input.txt", mode="r", encoding="utf-8") as fCargoInstructions:
        [CargoOrigins, Instructions] = fCargoInstructions.read().split("\n\n")
        fCargoInstructions.close()
        CargoQueues = parseCargoOrigins(CargoOrigins)
        Instructions = Instructions.split("\n")
        for Instruction in Instructions:
            [Repeat, Source, Dest] = instructionParser(Instruction)
            Repeat = int(Repeat)
            Source = int(Source)-1
            Dest = int(Dest)-1
            for i in range(Repeat):
                CargoQueues[Dest].put(CargoQueues[Source].get())
        topline=""
        for i in range(len(CargoQueues)):
            topentry = CargoQueues[i].get()
            CargoQueues[i].put(topentry)
            topline+=topentry
        print (topline)

    

def instructionParser(Instruction):
    res = re.search(r"move ([0-9]{1,2}) from ([0-9]{1,2}) to ([0-9]{1,2})", Instruction)
    return res.groups()

def parseCargoOrigins(CargoOrigins):
    CargoOriginLines = CargoOrigins.split("\n");
    CargoOriginXLegend = CargoOriginLines.pop()
    QCount = len(CargoOriginXLegend.split())
    CargoQs = []
    for i in range(QCount):
        CargoQs.append(LifoQueue())
    for CargoRow in range(len(CargoOriginLines)-1,-1,-1):
        CargoOriginLine = CargoOriginLines[CargoRow]
        for CargoCol in range(0, len(CargoOriginLine), 4):
            cargoItem = CargoOriginLine[CargoCol:CargoCol+4].strip()
            if cargoItem != "":
                CargoQs[CargoCol//4].put(cargoItem[1]) 
    return CargoQs

if __name__ == "__main__":
    main()