import React from "react"
import UpdatingDuration from "components/utils/UpdatingDuration"
import RunTimings, { Run } from "./RunTimings"

type RunStartedProps = {
  run: Run
}

const RunStarted: React.FC<RunStartedProps> = ({ run }) => (
  <UpdatingDuration
    start={run.created_at}
    tooltip={<RunTimings run={run} />}
    length={1}
    long
  />
)

export default RunStarted
