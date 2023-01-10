import { ApolloError } from "@apollo/client"
import {
  Grid,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  ListItemText,
  Divider,
  TextField,
} from "@mui/material"
import GraphError from "components/utils/GraphError"
import React, { ChangeEvent } from "react"
import { CronValue, Values } from "./CreateConnectionWizard"

type SetScheduleProps = {
  values: Values
  setValues: (values: Values) => void
  error?: ApolloError
}

const SetSchedule: React.FC<SetScheduleProps> = ({
  values,
  setValues,
  error,
}) => {
  const setCron =
    (field: keyof CronValue) => (event: ChangeEvent<HTMLInputElement>) => {
      let cron: CronValue = values?.schedules?.cron
        ? { ...values.schedules.cron }
        : {
            minutes: "*",
            hours: "*",
            day_of_week: "*",
            day_of_month: "*",
            month_of_year: "*",
          }

      cron[field] = event.target.value

      setValues({
        ...values,
        schedules: values.schedules
          ? { ...values.schedules, cron }
          : { type: "cron", cron },
      })
    }

  return (
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
            <>
              <Divider sx={{ my: 3 }} />
              <FormLabel>Schedule configuration</FormLabel>
              <TextField
                label="Minutes"
                helperText='Cron minutes to run. Use "*" for all. (Example: "0,30")'
                margin="normal"
                value={values.schedules?.cron?.minutes ?? ""}
                onChange={setCron("minutes")}
                fullWidth
              />
              <TextField
                label="Hours"
                helperText='Cron hours to run. Use "*" for all. (Example: "8,20")'
                margin="normal"
                value={values.schedules?.cron?.hours ?? ""}
                onChange={setCron("hours")}
                fullWidth
              />
              <TextField
                label="Days of the week"
                helperText='Cron days of the week to run. Use "*" for all. (Example: "0,5")'
                margin="normal"
                value={values.schedules?.cron?.day_of_week ?? ""}
                onChange={setCron("day_of_week")}
                fullWidth
              />
              <TextField
                label="Days of the month"
                helperText='Cron days of the month to run. Use "*" for all. (Example: "1,15")'
                margin="normal"
                value={values.schedules?.cron?.day_of_month ?? ""}
                onChange={setCron("day_of_month")}
                fullWidth
              />
              <TextField
                label="Months of the year"
                helperText='Cron months of the year to run. Use "*" for all. (Example: "0,6")'
                margin="normal"
                value={values.schedules?.cron?.month_of_year ?? ""}
                onChange={setCron("month_of_year")}
                fullWidth
              />
            </>
          )}
        </Grid>
      </Grid>
    </>
  )
}

export default SetSchedule
