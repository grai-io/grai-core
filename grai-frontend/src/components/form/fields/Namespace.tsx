import { gql, useQuery } from "@apollo/client"
import {
  Autocomplete,
  CircularProgress,
  InputAdornment,
  TextField,
} from "@mui/material"
import React from "react"
import { useParams } from "react-router-dom"
import {
  GetNamespaces,
  GetNamespacesVariables,
} from "./__generated__/GetNamespaces"

const GET_NAMESPACES = gql`
  query GetNamespaces($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      namespaces {
        id
        name
      }
    }
  }
`

type NamespaceProps = {
  value: string | null
  onChange: (value: string | null) => void
}

const Namespace: React.FC<NamespaceProps> = ({ value, onChange }) => {
  const { workspaceId } = useParams()
  const { data, loading } = useQuery<GetNamespaces, GetNamespacesVariables>(
    GET_NAMESPACES,
    {
      variables: {
        workspaceId: workspaceId ?? "",
      },
    }
  )

  const options = data?.workspace.namespaces.map((n: any) => n.name) ?? []

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
