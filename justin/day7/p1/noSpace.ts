import * as fs from "fs";

const file = fs.readFileSync("./input.txt", "utf-8").split("\n");
const cd = file.filter((a) => a.includes("$ cd"));

class folder {
  size: number = 0;
  contents = new Array();
  name: string;
  parent;
  constructor(name: any, parent: any) {
    this.name = name;
    this.parent = parent;
  }
}

let system = new Array();
system["/" as keyof object] = new folder("/", system["/" as keyof object]);
let path: string[] = [];
let i = 0;
let com;

while (file[i]) {
  if (file[i].includes("$ cd")) {
    com = file[i].slice(5);
    if (com == "/") {
      path = ["/"];
    } else if (com == "..") {
      path.length--;
    } else path.push(file[i].slice(5));
  } else if (file[i].includes("$ ls")) {
    let total = 0;
    i++;
    while (file[i]) {
      if (file[i][0] == "$") {
        i--;
        break;
      }
      if (file[i][0] == "d") {
        com = path.join("/") + "/" + file[i].slice(4);
        if (!system[com as keyof object]) {
          system[com as keyof object] = new folder(
            com,
            system[path.join("/") as keyof object]
          );
        }
        system[path.join("/") as keyof object].contents.push(
          system[com as keyof object]
        );
      } else {
        let matches = file[i].match(/[0-9]+/g);
        let size = matches ? parseInt(matches[0]) : 0;
        total += size;
      }
      i++;
    }
    system[path.join("/") as keyof object].size += total;
  }
  i++;
}

let q = [];
for (const element in system) {
  if (!system[element].contents.length) q.push(system[element]);
}
while (q.length) {
  let tempq = [];
  for (const item of q) {
    if (item.parent) {
      tempq.push(item.parent);
      item.parent.size += item.size;
    }
  }
  q = tempq;
}
let total = 0;
for (const element in system) {
  if (system[element].size <= 100000) total += system[element].size;
}

console.log(
  `The total size of all directories below 100000 bytes is: ${total}!`
);
