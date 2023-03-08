import React from "react"
import { Run } from "./RunFailures"

type RunSuccessRateProps = {
  run: Run | null
}

const RunSuccessRate: React.FC<RunSuccessRateProps> = ({ run }) => {
  const results = run?.metadata?.results

  if (!results?.length) return null

  if (results?.length === 0) return null

  const passes = results.filter(test => test.test_pass).length ?? 0
  const successRate = passes / results.length

  return <>{(successRate * 100).toFixed(2)}%</>
}
export default RunSuccessRate
