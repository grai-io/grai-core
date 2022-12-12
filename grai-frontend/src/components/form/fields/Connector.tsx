import { gql, useQuery } from "@apollo/client"
import {
  Autocomplete,
  CircularProgress,
  InputAdornment,
  TextField,
} from "@mui/material"
import React from "react"

const GET_CONNECTORS = gql`
  query GetConnectors {
    connectors {
      id
      name
    }
  }
`

export interface ConnectorType {
  id: string
  name: string
}

type ConnectorProps = {
  value: ConnectorType | null
  onChange: (value: ConnectorType | null) => void
}

const Connector: React.FC<ConnectorProps> = ({ value, onChange }) => {
  const { data, loading } = useQuery(GET_CONNECTORS)

  const options = data?.connectors ?? []

  const handleChange = (
    event: React.SyntheticEvent<Element, Event>,
    value: ConnectorType | null
  ) => onChange(value)

  return (
    <Autocomplete
      disablePortal
      options={options}
      getOptionLabel={value => value.name}
      value={value}
      onChange={handleChange}
      renderInput={params => (
        <TextField
          {...params}
          id="connector"
          fullWidth
          label="Connector"
          margin="normal"
          required
          InputProps={
            loading
              ? {
                  endAdornment: (
                    <InputAdornment position="end">
                      <CircularProgress />
                    </InputAdornment>
                  ),
                }
              : params.InputProps
          }
        />
      )}
    />
  )
}

export default Connector
