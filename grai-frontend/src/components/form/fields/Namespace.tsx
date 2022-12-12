import { gql, useQuery } from "@apollo/client"
import {
  Autocomplete,
  CircularProgress,
  InputAdornment,
  TextField,
} from "@mui/material"
import React from "react"

const GET_NAMESPACES = gql`
  query GetNamespaces {
    namespaces {
      id
      name
    }
  }
`

type NamespaceProps = {
  value: string | null
  onChange: (value: string | null) => void
}

const Namespace: React.FC<NamespaceProps> = ({ value, onChange }) => {
  const { data, loading } = useQuery(GET_NAMESPACES)

  const options = data?.namespaces.map((n: any) => n.name) ?? []

  const handleChange = (
    event: React.SyntheticEvent<Element, Event>,
    value: string | null
  ) => onChange(value)

  return (
    <Autocomplete
      freeSolo
      disablePortal
      options={options}
      value={value}
      onInputChange={handleChange}
      renderInput={params => (
        <TextField
          {...params}
          id="namespace"
          fullWidth
          label="Namespace"
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

export default Namespace
