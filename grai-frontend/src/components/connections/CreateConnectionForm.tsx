import { gql, useMutation } from "@apollo/client"
import {
  ArrowForward,
  CheckCircle,
  InsertDriveFileOutlined,
} from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import {
  Alert,
  AlertTitle,
  Box,
  Button,
  Divider,
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  ListItemText,
  Radio,
  RadioGroup,
  TextField,
  Typography,
} from "@mui/material"
import { ConnectorType } from "components/form/fields/Connector"
import GraphError from "components/utils/GraphError"
import WizardLayout, { WizardSteps } from "components/wizards/WizardLayout"
import React, { useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import ConnectionsMetadata from "./ConnectionsMetadata"
import ConnectorList from "./ConnectorList"
import CreateConnectionHelp from "./CreateConnectionHelp"
import {
  CreateConnection,
  CreateConnectionVariables,
} from "./__generated__/CreateConnection"

export const CREATE_CONNECTION = gql`
  mutation CreateConnection(
    $workspaceId: ID!
    $connectorId: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
    $schedules: JSON
    $is_active: Boolean
  ) {
    createConnection(
      workspaceId: $workspaceId
      connectorId: $connectorId
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
      schedules: $schedules
      is_active: $is_active
    ) {
      id
      connector {
        id
        name
      }
      namespace
      name
      metadata
      is_active
      created_at
      updated_at
    }
  }
`

const databases = [
  {
    title: "PostreSQL",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/245cb2ccbc976d6dc38d90456ca1fd7cdbcb2dc6-2424x2500.svg",
  },
  {
    title: "Snowflake",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/a4ac9f5f978ab2446fc17bf116067cb7c74116a2-960x952.png",
  },
  {
    title: "Amazon Redshift",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/f3e8edc5f92315c09202e01a28f206e777084c12-512x512.svg",
    disabled: true,
  },
  {
    title: "Google BigQuery",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/2a4f3d940e21dfa356bd993177586dab5e1b628f-2500x2500.svg",
    disabled: true,
  },
  {
    title: "Microsoft SQL Server",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/95bced9d0a4f668ceea0442a15c2cb4fdcb38b7e-452x452.png",
    disabled: true,
  },
  {
    title: "MongoDB",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/804ef5c917633c58b18f6cfc0d654b637cbc9a0e-128x128.png",
    disabled: true,
  },
  {
    title: "MySQL",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/e4d7a37a2425ce7e012e23fdb4f53d985e18a4a3-1280x1280.png",
    disabled: true,
  },
]

const data_tools = [
  {
    title: "dbt",
    iconSrc: "/images/dbt-logo.png",
  },
  {
    title: "Fivetran",
    iconSrc: "/images/fivetran-logo.png",
  },
  {
    title: "Stitch",
    iconSrc: "/images/stitch-logo.png",
    disabled: true,
  },
]

const others = [
  {
    title: "Flat File",
    icon: <InsertDriveFileOutlined />,
  },
]

type CronValue = {
  minutes: string
  hours: string
  day_of_week: string
  day_of_month: string
  month_of_year: string
}

type SchedulesValues = {
  type: string | null
  cron?: CronValue
}

export type Values = {
  connector: ConnectorType | null
  namespace: string
  name: string
  metadata: any
  secrets: any
  schedules: SchedulesValues | null
}

const CreateConnectionForm: React.FC = () => {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

  const [createConnection, { loading, error }] = useMutation<
    CreateConnection,
    CreateConnectionVariables
  >(CREATE_CONNECTION)

  const defaultValues: Values = {
    connector: null,
    namespace: "",
    name: "",
    metadata: null,
    secrets: null,
    schedules: null,
  }

  const [values, setValues] = useState<Values>(defaultValues)

  const handleSubmit = () =>
    createConnection({
      variables: {
        workspaceId: workspaceId ?? "",
        connectorId: values.connector?.id ?? "",
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets,
        schedules: values.schedules,
        is_active: true,
      },
    })
      .then(res =>
        navigate(
          `/workspaces/${workspaceId}/connections/${res.data?.createConnection.id}`
        )
      )
      .catch(() => {})

  const setCron = (field: keyof CronValue, value: string) => {
    let cron: CronValue = values?.schedules?.cron
      ? { ...values.schedules.cron }
      : {
          minutes: "*",
          hours: "*",
          day_of_week: "*",
          day_of_month: "*",
          month_of_year: "*",
        }

    cron[field] = value

    setValues({
      ...values,
      schedules: values.schedules
        ? { ...values.schedules, cron }
        : { type: "cron", cron },
    })
  }

  const handleSelect = (setActiveStep: (step: number) => void) => {
    setValues({
      ...values,
      connector: {
        id: "768aea48-1146-4f14-9005-40e89504f4b3",
        name: "Postgres",
        metadata: {
          fields: [
            {
              name: "dbname",
              label: "Database Name",
              required: true,
            },
            {
              name: "user",
              required: true,
            },
            {
              name: "password",
              secret: true,
              required: true,
            },
            {
              name: "host",
              required: true,
            },
            {
              name: "port",
              default: 5432,
              required: true,
            },
          ],
        },
      },
    })
    setActiveStep(1)
  }

  const steps: WizardSteps = [
    {
      title: "Select connector",
      subTitle: "Select a connector",
      actionText: "Click on a connector to continue",
      element: ({ setActiveStep }) => (
        <>
          <ConnectorList
            title="Databases"
            connectors={databases}
            onSelect={() => handleSelect(setActiveStep)}
          />
          <ConnectorList
            title="Data tools"
            connectors={data_tools}
            onSelect={() => handleSelect(setActiveStep)}
          />
          <ConnectorList
            title="Other"
            connectors={others}
            onSelect={() => handleSelect(setActiveStep)}
          />
        </>
      ),
    },
    {
      title: "Setup connection",
      subTitle: (
        <Box sx={{ display: "flex" }}>
          <img
            src="https://cdn.sanity.io/images/pwmfmi47/production/245cb2ccbc976d6dc38d90456ca1fd7cdbcb2dc6-2424x2500.svg"
            alt="PostgreSQL logo"
            style={{ height: 28, width: 28 }}
          />
          <Typography variant="h5" sx={{ ml: 2 }}>
            Connect to PostgreSQL
          </Typography>
        </Box>
      ),
      element: (
        <Grid container sx={{ mt: 5 }}>
          <Grid item md={8} sx={{ pr: 3 }}>
            <TextField
              label="Namespace"
              margin="normal"
              value={values.namespace}
              onChange={event =>
                setValues({ ...values, namespace: event.target.value })
              }
              required
              fullWidth
            />
            <TextField
              label="Name"
              margin="normal"
              value={values.name}
              onChange={event =>
                setValues({ ...values, name: event.target.value })
              }
              required
              fullWidth
            />
            {values.connector && (
              <ConnectionsMetadata
                connector={values.connector}
                metadata={values.metadata}
                secrets={values.secrets}
                onChangeMetadata={value =>
                  setValues({ ...values, metadata: value })
                }
                onChangeSecrets={value =>
                  setValues({ ...values, secrets: value })
                }
              />
            )}
          </Grid>
          <Grid item md={4} sx={{}}>
            <CreateConnectionHelp />
          </Grid>
        </Grid>
      ),
      actionButtons: opts => (
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          endIcon={<ArrowForward />}
          onClick={opts.forwardStep}
        >
          Continue
        </Button>
      ),
    },
    {
      title: "Test connection",
      subTitle: (
        <Box sx={{ display: "flex" }}>
          <img
            src="https://cdn.sanity.io/images/pwmfmi47/production/245cb2ccbc976d6dc38d90456ca1fd7cdbcb2dc6-2424x2500.svg"
            alt="PostgreSQL logo"
            style={{ height: 28, width: 28 }}
          />
          <Typography variant="h5" sx={{ ml: 2 }}>
            Test connection to PostgreSQL
          </Typography>
        </Box>
      ),
      element: (
        <Grid container sx={{ mt: 5 }}>
          <Grid item md={8} sx={{ pr: 3 }}>
            <Box sx={{ display: "flex" }}>
              <CheckCircle color="success" />
              <Typography
                variant="body2"
                sx={{ ml: 2, color: theme => theme.palette.success.main }}
              >
                SUCCESS
              </Typography>
              <Typography variant="body2" sx={{ ml: 5 }}>
                Validate ability to access PostgreSQL
              </Typography>
            </Box>
            <Divider sx={{ mt: 2, mb: 3 }} />
            <Alert severity="success">
              <AlertTitle>All tests successfully passed!</AlertTitle>Continue to
              complete setting up your PostgreSQL connection.
            </Alert>
          </Grid>
          <Grid item md={4} sx={{}}>
            <CreateConnectionHelp />
          </Grid>
        </Grid>
      ),
      actionButtons: opts => (
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          endIcon={<ArrowForward />}
          onClick={opts.forwardStep}
        >
          Continue
        </Button>
      ),
    },
    {
      title: "Set schedule",
      subTitle: "Set a schedule for this connection",
      element: (
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
                    control={<Radio sx={{ mr: 1 }} />}
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
                    onChange={event => setCron("minutes", event.target.value)}
                    fullWidth
                  />
                  <TextField
                    label="Hours"
                    helperText='Cron hours to run. Use "*" for all. (Example: "8,20")'
                    margin="normal"
                    value={values.schedules?.cron?.hours ?? ""}
                    onChange={event => setCron("minutes", event.target.value)}
                    fullWidth
                  />
                  <TextField
                    label="Days of the week"
                    helperText='Cron days of the week to run. Use "*" for all. (Example: "0,5")'
                    margin="normal"
                    value={values.schedules?.cron?.day_of_week ?? ""}
                    onChange={event =>
                      setCron("day_of_week", event.target.value)
                    }
                    fullWidth
                  />
                  <TextField
                    label="Days of the month"
                    helperText='Cron days of the month to run. Use "*" for all. (Example: "1,15")'
                    margin="normal"
                    value={values.schedules?.cron?.day_of_month ?? ""}
                    onChange={event =>
                      setCron("day_of_month", event.target.value)
                    }
                    fullWidth
                  />
                  <TextField
                    label="Months of the year"
                    helperText='Cron months of the year to run. Use "*" for all. (Example: "0,6")'
                    margin="normal"
                    value={values.schedules?.cron?.month_of_year ?? ""}
                    onChange={event =>
                      setCron("month_of_year", event.target.value)
                    }
                    fullWidth
                  />
                </>
              )}
            </Grid>
          </Grid>
        </>
      ),
      actionButtons: (
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          loading={loading}
          onClick={handleSubmit}
        >
          Finish
        </LoadingButton>
      ),
    },
  ]

  return (
    <WizardLayout
      title="Create Connection"
      steps={steps}
      closeRoute={workspaceId => `/workspaces/${workspaceId}/connections`}
    />
  )
}

export default CreateConnectionForm
