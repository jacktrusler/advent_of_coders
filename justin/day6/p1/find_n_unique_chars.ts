export function findNChars(string: string, n: number) {
  //Finds end of the first occurence of n distinct Characters; returns null if no match
  let p1 = 0,
    p2 = n;
  while (string[p2]) {
    if (new Set(string.substring(p1, p2)).size == n) return p2;
    p1++;
    p2++;
  }
  return null;
}
