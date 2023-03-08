import React from "react"

export interface RunMetadata {
  results?: {
    test_pass?: boolean
  }[]
}

export interface Run {
  metadata: RunMetadata | null
}

type RunFailuresProps = {
  run: Run | null
}

const RunFailures: React.FC<RunFailuresProps> = ({ run }) => (
  <>{run?.metadata?.results?.filter(test => !test.test_pass).length}</>
)

export default RunFailures
