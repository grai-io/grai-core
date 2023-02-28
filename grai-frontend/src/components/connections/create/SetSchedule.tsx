import React from "react"
import { ApolloError } from "@apollo/client"
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
import { Values } from "./CreateConnectionWizard"
import SetCron from "./SetCron"
import ScheduleHelp from "../schedule/ScheduleHelp"

type SetScheduleProps = {
  opts: ElementOptions
  values: Values
  setValues: (values: Values) => void
  loading?: boolean
  error?: ApolloError
  onSubmit: () => void
}

const SetSchedule: React.FC<SetScheduleProps> = ({
  opts,
  values,
  setValues,
  loading,
  error,
  onSubmit,
}) => (
  <>
    <WizardSubtitle title="Set a schedule for this connection" />
    {error && <GraphError error={error} />}
    <Grid container sx={{ pt: 3 }}>
      <Grid item md={8}>
        <FormControl>
          <FormLabel sx={{ mb: 1 }}>Schedule type</FormLabel>
          <RadioGroup
            value={values.schedules?.type ?? ""}
            onChange={event =>
              setValues({
                ...values,
                schedules: {
                  ...values.schedules,
                  type: event.target.value,
                },
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
        {values.schedules?.type === "cron" && (
          <SetCron
            schedules={values.schedules}
            values={values}
            setValues={setValues}
          />
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
        onClick={onSubmit}
      >
        Finish
      </LoadingButton>
    </WizardBottomBar>
  </>
)

export default SetSchedule
