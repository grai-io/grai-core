import { gql, useQuery } from "@apollo/client"
import {
  Autocomplete,
  CircularProgress,
  InputAdornment,
  TextField,
} from "@mui/material"
import React from "react"
import { GetConnectors } from "./__generated__/GetConnectors"

const GET_CONNECTORS = gql`
  query GetConnectors {
    connectors {
      id
      name
      metadata
    }
  }
`

export interface ConnectorMetadataField {
  name: string
  label?: string
  secret?: boolean
  required?: boolean
  default?: string | number
}

export interface ConnectorMetadata {
  fields?: ConnectorMetadataField[]
}

export interface ConnectorType {
  id: string
  name: string
  metadata: ConnectorMetadata | null | undefined
}

type ConnectorProps = {
  value: ConnectorType | null
  onChange: (value: ConnectorType | null) => void
}

const Connector: React.FC<ConnectorProps> = ({ value, onChange }) => {
  const { data, loading } = useQuery<GetConnectors>(GET_CONNECTORS)

  const options = data?.connectors ?? []

  const handleChange = (
    event: React.SyntheticEvent<Element, Event>,
    value: ConnectorType | null
  ) => onChange(value)

  return (
    <Autocomplete<ConnectorType>
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
