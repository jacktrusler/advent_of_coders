function recurse(arr) {
  if (!Array.isArray(arr)) {
    recurse([arr]) 
  }
  return arr
}

console.log(recurse(5))

export { recurse }
