import { Accept } from "react-dropzone"

const getAccept = (extension: string | null | undefined): Accept => {
  if (extension === "json")
    return {
      "application/json": [".json"],
    }

  if (extension === "yaml")
    return {
      "application/yaml": [".yaml", ".yml"],
    }

  if (extension === "flat-file")
    return {
      "application/octet-stream": [".csv", ".parquet", ".feather", ".arrow"],
    }

  return {
    "*": ["*"],
  }
}

export default getAccept
