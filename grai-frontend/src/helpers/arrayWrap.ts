const arrayWrap = <T>(value: T | T[]): T[] =>
  Array.isArray(value) ? value : [value]

export const arrayWrapDefault = <T>(
  value: T | NonNullable<T>[] | undefined,
  defaultValue: NonNullable<T>[] = [],
): NonNullable<T>[] => (value ? arrayWrap(value) : defaultValue)

export default arrayWrap
