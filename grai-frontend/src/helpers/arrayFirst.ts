const arrayFirst = <T>(value: T | T[]): T | undefined =>
  Array.isArray(value) ? value[0] : value

export default arrayFirst
