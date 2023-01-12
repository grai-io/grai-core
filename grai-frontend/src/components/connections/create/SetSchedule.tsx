import { ApolloError } from "@apollo/client"
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
import React from "react"
import { Values } from "./CreateConnectionWizard"
import SetCron from "./SetCron"

type SetScheduleProps = {
  values: Values
  setValues: (values: Values) => void
  error?: ApolloError
}

const SetSchedule: React.FC<SetScheduleProps> = ({
  values,
  setValues,
  error,
}) => (
  <>
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
                  primary="Custom resurrence"
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
    </Grid>
  </>
)

export default SetSchedule
