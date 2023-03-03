import React, { ChangeEvent } from "react"
import { Divider, FormLabel, TextField } from "@mui/material"
import { CronValue, Values } from "./SetSchedule"

type SetCronProps = {
  values: Values
  setValues: (values: Values) => void
}

const SetCron: React.FC<SetCronProps> = ({ values, setValues }) => {
  const setCron =
    (field: keyof CronValue) => (event: ChangeEvent<HTMLInputElement>) => {
      let cron: CronValue = values?.cron
        ? { ...values.cron }
        : {
            minutes: "*",
            hours: "*",
            day_of_week: "*",
            day_of_month: "*",
            month_of_year: "*",
          }

      cron[field] = event.target.value

      values && setValues({ ...values, cron })
    }

  return (
    <>
      <Divider sx={{ my: 3 }} />
      <FormLabel>Schedule configuration</FormLabel>
      <TextField
        label="Minutes"
        helperText='Cron minutes to run. Use "*" for all. (Example: "0,30")'
        margin="normal"
        value={values?.cron?.minutes ?? ""}
        onChange={setCron("minutes")}
        fullWidth
      />
      <TextField
        label="Hours"
        helperText='Cron hours to run. Use "*" for all. (Example: "8,20")'
        margin="normal"
        value={values?.cron?.hours ?? ""}
        onChange={setCron("hours")}
        fullWidth
      />
      <TextField
        label="Days of the week"
        helperText='Cron days of the week to run. Use "*" for all. (Example: "0,5")'
        margin="normal"
        value={values?.cron?.day_of_week ?? ""}
        onChange={setCron("day_of_week")}
        fullWidth
      />
      <TextField
        label="Days of the month"
        helperText='Cron days of the month to run. Use "*" for all. (Example: "1,15")'
        margin="normal"
        value={values?.cron?.day_of_month ?? ""}
        onChange={setCron("day_of_month")}
        fullWidth
      />
      <TextField
        label="Months of the year"
        helperText='Cron months of the year to run. Use "*" for all. (Example: "0,6")'
        margin="normal"
        value={values?.cron?.month_of_year ?? ""}
        onChange={setCron("month_of_year")}
        fullWidth
      />
    </>
  )
}

export default SetCron
