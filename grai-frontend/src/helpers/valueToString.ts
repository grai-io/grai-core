const valueToString = (value: any): string => {
  switch (typeof value) {
    case "string":
      return value
    case "boolean":
      return value ? "yes" : "no"
  }

  return JSON.stringify(value)
}

export default valueToString
