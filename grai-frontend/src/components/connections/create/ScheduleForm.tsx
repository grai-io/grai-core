import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import {
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  ListItemText,
  Box,
} from "@mui/material"
import GraphError from "components/utils/GraphError"
import {
  UpdateConnectionInitialSchedule,
  UpdateConnectionInitialScheduleVariables,
} from "./__generated__/UpdateConnectionInitialSchedule"
import SetCron from "./SetCron"

export const UPDATE_CONNECTION = gql`
  mutation UpdateConnectionInitialSchedule(
    $id: ID!
    $schedules: JSON
    $is_active: Boolean!
  ) {
    updateConnection(id: $id, schedules: $schedules, is_active: $is_active) {
      id
      schedules
      is_active
    }
  }
`

export type CronValue = {
  minutes: string
  hours: string
  day_of_week: string
  day_of_month: string
  month_of_year: string
}

export type Values = {
  type: string | null
  cron?: CronValue
} | null

interface Connection {
  id: string
}

type ScheduleFormProps = {
  connection: Connection
  onComplete: () => void
}

const ScheduleForm: React.FC<ScheduleFormProps> = ({
  connection,
  onComplete,
}) => {
  const [values, setValues] = useState<Values>(null)

  const [updateConnection, { loading, error }] = useMutation<
    UpdateConnectionInitialSchedule,
    UpdateConnectionInitialScheduleVariables
  >(UPDATE_CONNECTION)

  const handleSubmit = () => {
    updateConnection({
      variables: {
        id: connection?.id,
        schedules: values,
        is_active: true,
      },
    })
      .then(() => onComplete())
      .catch(() => {})
  }

  return (
    <>
      {error && <GraphError error={error} />}
      <FormControl>
        <FormLabel sx={{ mb: 1 }}>Schedule type</FormLabel>
        <RadioGroup
          value={values?.type ?? ""}
          onChange={event =>
            setValues({
              ...values,
              type: event.target.value,
            })
          }
        >
          <FormControlLabel
            value=""
            control={<Radio sx={{ mr: 1 }} />}
            label={
              <ListItemText
                primary="Manual"
                secondary="Trigger your sync manually in the Grai app or using our API"
              />
            }
            sx={{ my: 1 }}
          />
          <FormControlLabel
            value="interval"
            control={<Radio sx={{ mr: 1 }} />}
            label={
              <ListItemText
                primary="Interval"
                secondary="Schedule your sync to run on a set interval (e.g., once per hour)"
              />
            }
            sx={{ my: 1 }}
            disabled
          />
          <FormControlLabel
            value="custom"
            control={<Radio sx={{ mr: 1 }} />}
            label={
              <ListItemText
                primary="Custom recurrence"
                secondary="Schedule your sync to run on specific days (e.g., Mondays at 9am)"
              />
            }
            sx={{ my: 1 }}
            disabled
          />
          <FormControlLabel
            value="cron"
            control={<Radio sx={{ mr: 1 }} data-testid="cron-expression" />}
            label={
              <ListItemText
                primary="Cron expression"
                secondary="Schedule your sync using a cron expression"
              />
            }
            sx={{ my: 1 }}
          />
        </RadioGroup>
      </FormControl>
      {values?.type === "cron" && (
        <SetCron values={values} setValues={setValues} />
      )}
      <Box sx={{ textAlign: "right" }}>
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{
            minWidth: 120,
            backgroundColor: "#FC6016",
            boxShadow: "0px 4px 6px 0px rgba(252, 96, 22, 0.20)",
          }}
          loading={loading}
          onClick={handleSubmit}
        >
          Finish
        </LoadingButton>
      </Box>
    </>
  )
}

export default ScheduleForm
