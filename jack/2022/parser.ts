let j = 0;
let i = 0;
function parser(lhs: string[], rhs: string[]): boolean {
  while (lhs.length > 0) {
    if (/[0-9]/.test(lhs[i]) && /[0-9]/.test(rhs[j])) {
      if (parseInt(lhs[i]) > parseInt(rhs[j])) {
        return false;
      }
    }
    if (lhs[i] === '[' && /[0-9]/.test(rhs[j])) {
      let testArr = lhs.splice(i, lhs.indexOf(']'))
      for (const num of testArr) {
        if (parseInt(num) > parseInt(rhs[j])) { return false; }
      }
    }
    if (rhs[j] === '[' && /[0-9]/.test(lhs[i])) {
      let testArr = rhs.splice(j, rhs.indexOf(']'))
      for (const num of testArr) {
        if (parseInt(lhs[i]) > parseInt(num)) { return false; }
      }
    }
    if (rhs.length === 0 && lhs.length !== 0) return false;
    lhs.shift()
    rhs.shift()
  }
  return true
}
