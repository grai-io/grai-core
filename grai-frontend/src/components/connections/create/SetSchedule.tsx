import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import {
  Grid,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  ListItemText,
} from "@mui/material"
import GraphError from "components/utils/GraphError"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import {
  UpdateConnectionInitialSchedule,
  UpdateConnectionInitialScheduleVariables,
} from "./__generated__/UpdateConnectionInitialSchedule"
import { Connection } from "./CreateConnectionWizard"
import SetCron from "./SetCron"
import ScheduleHelp from "../schedule/ScheduleHelp"

export const UPDATE_CONNECTION = gql`
  mutation UpdateConnectionInitialSchedule(
    $id: ID!
    $schedules: JSON
    $is_active: Boolean!
  ) {
    updateConnection(
      id: $id
      schedules: $schedules
      is_active: $is_active
      temp: false
    ) {
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

type SetScheduleProps = {
  opts: ElementOptions
  connection: Connection
  onComplete: () => void
}

const SetSchedule: React.FC<SetScheduleProps> = ({
  opts,
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
      <WizardSubtitle title="Set a schedule for this connection" />
      {error && <GraphError error={error} />}
      <Grid container sx={{ pt: 3 }}>
        <Grid item md={8}>
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
        </Grid>
        <Grid item md={4}>
          <ScheduleHelp />
        </Grid>
      </Grid>
      <WizardBottomBar opts={opts}>
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          loading={loading}
          onClick={handleSubmit}
        >
          Finish
        </LoadingButton>
      </WizardBottomBar>
    </>
  )
}

export default SetSchedule
