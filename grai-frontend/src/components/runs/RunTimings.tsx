import { Typography } from "@mui/material"
import { DateTime } from "luxon"
import React from "react"

export interface Run {
  created_at: string
  started_at: string | null
  finished_at: string | null
}

type RunTimingsProps = { run: Run }

const RunTimings: React.FC<RunTimingsProps> = ({ run }) => (
  <>
    <Typography variant="body2" color="inherit">
      Created:{" "}
      {DateTime.fromISO(run.created_at).toLocaleString(
        DateTime.DATETIME_FULL_WITH_SECONDS
      )}
    </Typography>
    {run.started_at && (
      <Typography variant="body2" color="inherit">
        Started:{" "}
        {DateTime.fromISO(run.started_at).toLocaleString(
          DateTime.DATETIME_FULL_WITH_SECONDS
        )}
      </Typography>
    )}
    {run.finished_at && (
      <Typography variant="body2" color="inherit">
        Finished:{" "}
        {DateTime.fromISO(run.finished_at).toLocaleString(
          DateTime.DATETIME_FULL_WITH_SECONDS
        )}
      </Typography>
    )}
  </>
)

export default RunTimings
