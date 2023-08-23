const arrayWrap = <T>(value: T | T[]): T[] =>
  Array.isArray(value) ? value : [value]

export default arrayWrap
