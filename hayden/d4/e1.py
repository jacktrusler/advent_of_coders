def main():
    with open(file="jannies.txt", mode="r", encoding="utf-8") as fJanny:
        jannyLaps = 0
        completeSectionJannyLaps = 0
        jannyAssignments = fJanny.readlines()
        for jannyAssignment in jannyAssignments:
            jCrewAssignments = jannyAssignment.strip().split(",")
            lJannyAssignment= set(expandJannyIDs(jCrewAssignments[0]))
            rJannyAssignment= set(expandJannyIDs(jCrewAssignments[1]))
            if lJannyAssignment & rJannyAssignment:
                jannyLaps += 1
            if lJannyAssignment <= rJannyAssignment or rJannyAssignment <= lJannyAssignment:
                completeSectionJannyLaps += 1
        print("Any Janny Overlaps ", jannyLaps)
        print("Complete failures to plan ", completeSectionJannyLaps)
def expandJannyIDs(rangeStr):
    rangeVals = rangeStr.split("-")
    return range(int(rangeVals[0]),int(rangeVals[1])+1)

if __name__ == "__main__":
    main()