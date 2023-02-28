import React, { ChangeEvent } from "react"
import { Divider, FormLabel, TextField } from "@mui/material"
import { CronValue, SchedulesValues, Values } from "./CreateConnectionWizard"

type SetCronProps = {
  schedules: SchedulesValues
  values: Values
  setValues: (values: Values) => void
}

const SetCron: React.FC<SetCronProps> = ({ schedules, values, setValues }) => {
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
        schedules: { ...schedules, cron },
      })
    }

  return (
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
  )
}

export default SetCron
