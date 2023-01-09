import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import {
  Checkbox,
  Dialog,
  DialogContent,
  FormControl,
  FormControlLabel,
  FormGroup,
  FormLabel,
  Radio,
  RadioGroup,
  TextField,
} from "@mui/material"
import BootstrapDialogTitle from "components/dialogs/DialogTitle"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import React, { useState } from "react"
import { Connection } from "./ConnectionSchedule"
import {
  UpdateConnectionSchedule,
  UpdateConnectionScheduleVariables,
} from "./__generated__/UpdateConnectionSchedule"

export const UPDATE_CONNECTION = gql`
  mutation UpdateConnectionSchedule(
    $id: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
    $schedules: JSON
    $is_active: Boolean
  ) {
    updateConnection(
      id: $id
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
      schedules: $schedules
      is_active: $is_active
    ) {
      id
      namespace
      name
      metadata
      schedules
      is_active
      created_at
      updated_at
    }
  }
`

type CronValue = {
  minutes: string
  hours: string
  day_of_week: string
  day_of_month: string
  month_of_year: string
}

type Values = {
  type: string | null
  cron?: CronValue
}

type EditScheduleDialogProps = {
  connection: Connection
  open: boolean
  onClose: () => void
}

const EditScheduleDialog: React.FC<EditScheduleDialogProps> = ({
  connection,
  open,
  onClose,
}) => {
  const [is_active, setIsActive] = useState(connection.is_active)
  const [values, setValues] = useState<Values>(
    connection.schedules
      ? connection.schedules
      : {
          type: "",
        }
  )

  const [updateConnection, { loading, error }] = useMutation<
    UpdateConnectionSchedule,
    UpdateConnectionScheduleVariables
  >(UPDATE_CONNECTION)

  const handleSubmit = () =>
    updateConnection({
      variables: {
        ...connection,
        schedules: values.type === "" ? null : values,
        is_active,
        secrets: {},
      },
    }).then(() => onClose())

  const setCron = (field: keyof CronValue, value: string) => {
    let cron: CronValue = values?.cron ?? {
      minutes: "*",
      hours: "*",
      day_of_week: "*",
      day_of_month: "*",
      month_of_year: "*",
    }

    cron[field] = value

    setValues({ ...values, cron })
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <BootstrapDialogTitle onClose={onClose}>
        Edit Schedule
      </BootstrapDialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        <Form onSubmit={handleSubmit}>
          <FormControl>
            <FormLabel sx={{ mb: 1 }}>Schedule type</FormLabel>
            <RadioGroup
              value={values.type ?? ""}
              onChange={event =>
                setValues({
                  ...values,
                  type: event.target.value,
                })
              }
            >
              <FormControlLabel value="" control={<Radio />} label="Manual" />
              <FormControlLabel
                value="interval"
                control={<Radio />}
                label="Interval"
                disabled
              />
              <FormControlLabel
                value="custom"
                control={<Radio />}
                label="Custom resurrence"
                disabled
              />
              <FormControlLabel
                value="cron"
                control={<Radio />}
                label="Cron expression"
              />
            </RadioGroup>
          </FormControl>
          {values.type === "cron" && (
            <>
              <TextField
                label="Minutes"
                helperText='Cron minutes to run. Use "*" for all. (Example: "0,30")'
                margin="normal"
                value={values.cron?.minutes ?? ""}
                onChange={event => setCron("minutes", event.target.value)}
                fullWidth
              />
              <TextField
                label="Hours"
                helperText='Cron hours to run. Use "*" for all. (Example: "8,20")'
                margin="normal"
                value={values.cron?.hours ?? ""}
                onChange={event => setCron("minutes", event.target.value)}
                fullWidth
              />
              <TextField
                label="Days of the week"
                helperText='Cron days of the week to run. Use "*" for all. (Example: "0,5")'
                margin="normal"
                value={values.cron?.day_of_week ?? ""}
                onChange={event => setCron("day_of_week", event.target.value)}
                fullWidth
              />
              <TextField
                label="Days of the month"
                helperText='Cron days of the month to run. Use "*" for all. (Example: "1,15")'
                margin="normal"
                value={values.cron?.day_of_month ?? ""}
                onChange={event => setCron("day_of_month", event.target.value)}
                fullWidth
              />
              <TextField
                label="Months of the year"
                helperText='Cron months of the year to run. Use "*" for all. (Example: "0,6")'
                margin="normal"
                value={values.cron?.month_of_year ?? ""}
                onChange={event => setCron("month_of_year", event.target.value)}
                fullWidth
              />
            </>
          )}
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  checked={values.type === "" ? false : is_active}
                  onChange={event => setIsActive(event.target.checked)}
                  disabled={values.type === ""}
                />
              }
              label="Enabled"
            />
          </FormGroup>
          <LoadingButton
            variant="contained"
            type="submit"
            loading={loading}
            sx={{ mt: 2 }}
          >
            Save
          </LoadingButton>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default EditScheduleDialog
