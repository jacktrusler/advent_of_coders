import run from "aocrunner";

// Let's Get it! 🧝‍♀️🧝‍♂️

const parseInput = (rawInput: string) => {
  return rawInput.split("\n");
};

class Workshop {
  elfPairs: ElfPair[];
  constructor(manifest: string[]) {
    this.elfPairs = manifest.map((elfAssignmentPair) => {
      const elvesOnAssignment = elfAssignmentPair
        .split(",")
        .map((elfAssignment) => new Elf(elfAssignment));
      return new ElfPair(elvesOnAssignment);
    });
  }
  get matchingAssignmentPairs() {
    const clashingAssignments = this.elfPairs.filter(
      (elfPair) => elfPair.hasOverlappingAssignment,
    );
    return clashingAssignments.length;
  }
}

class ElfPair {
  Snowflake: Elf;
  Pinecone: Elf;
  constructor(elves: Elf[]) {
    this.Snowflake = elves[0];
    this.Pinecone = elves[1];
  }
  get hasOverlappingAssignment() {
    return this.Snowflake.hasAssignmentOverlap(this.Pinecone.assignment);
  }
}

class Elf {
  assignment: Assignment;
  constructor(scribbledAssignment: string) {
    const [scribbledStart, scribbledEnd] = scribbledAssignment.split("-");
    this.assignment = new Assignment(scribbledStart, scribbledEnd);
  }

  /*

         .-""""-.
       .'          '.
      /   O      O   \
     :                :
     |                |
     : ',          ,' :
      \  '-......-'  /
       '.          .'
         '-......-'
      |`-........-'`|
      |              |
      :              :
      |              |
      :              :
       \            /
        `""""""""""`
      |`-........-'`|
      |              |
      :              :
      |              |
      :              :
       \            /
        `""""""""""`
========================================
======= Part 1 - Total Overlap! ========
========================================
 
*/
  hasTotalAssignmentOverlap(assignmentToTest: Assignment) {
    const hasOverlap =
      this.assignment.start <= assignmentToTest.start &&
      this.assignment.end >= assignmentToTest.end;
    const hasUnderlap =
      this.assignment.start >= assignmentToTest.start &&
      this.assignment.end <= assignmentToTest.end;
    return hasOverlap || hasUnderlap;
  }

  /*

      /\   /\
     /  \ /  \
    /    Y    \
    \    |    /
     \   |   /
      \  |  /
       \ | /
        \|/

 ========================================
 ========== Part 2 - Some Lap! ==========
 ========================================
 
*/
  hasAssignmentOverlap(assignmentToTest: Assignment) {
    const ohGod =
      this.assignment.start >= assignmentToTest.start &&
      this.assignment.start >= assignmentToTest.end &&
      this.assignment.end <= assignmentToTest.end;
    const isThisWhatThey =
      this.assignment.end >= assignmentToTest.start &&
      this.assignment.end >= assignmentToTest.end &&
      this.assignment.start <= assignmentToTest.end;
    const callALogicOmelette =
      assignmentToTest.start >= this.assignment.start &&
      assignmentToTest.start >= this.assignment.end &&
      assignmentToTest.end <= this.assignment.end;
    const orIsThatSomethingDifferent =
      assignmentToTest.end >= this.assignment.start &&
      assignmentToTest.end >= this.assignment.end &&
      assignmentToTest.start <= this.assignment.end;

    return (
      ohGod ||
      isThisWhatThey ||
      callALogicOmelette ||
      orIsThatSomethingDifferent
    );
  }
}

class Assignment {
  start: number;
  end: number;
  constructor(scribbledStart: string, scribbledEnd: string) {
    this.start = parseInt(scribbledStart);
    this.end = parseInt(scribbledEnd);
  }
}

const part1 = (rawInput: string) => {
  const factoryManifest = parseInput(rawInput);
  const workshop = new Workshop(factoryManifest);

  return workshop.matchingAssignmentPairs;
};

const part2 = (rawInput: string) => {
  const factoryManifest = parseInput(rawInput);
  const workshop = new Workshop(factoryManifest);

  return workshop.matchingAssignmentPairs;
};

run({
  part1: {
    tests: [
      {
        input: `2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8`,
        expected: 2,
      },
    ],
    solution: part1,
  },
  part2: {
    tests: [
      {
        input: `2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8`,
        expected: 4,
      },
    ],
    solution: part2,
  },
  trimTestInputs: true,
  onlyTests: false,
});
