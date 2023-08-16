import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Grid } from "@mui/material"
import { useSnackbar } from "notistack"
import {
  UpdateSource as UpdateSourceType,
  UpdateSourceVariables,
} from "./__generated__/UpdateSource"
import SourceForm, { Values } from "./SourceForm"

export const UPDATE_SOURCE = gql`
  mutation UpdateSource($sourceId: ID!, $name: String!, $priority: Int!) {
    updateSource(id: $sourceId, name: $name, priority: $priority) {
      id
      name
      priority
    }
  }
`

export interface Source {
  id: string
  name: string
  priority: number
}

type UpdateSourceProps = {
  source: Source
}

const UpdateSource: React.FC<UpdateSourceProps> = ({ source }) => {
  const { enqueueSnackbar } = useSnackbar()
  const [updateSource, { loading, error }] = useMutation<
    UpdateSourceType,
    UpdateSourceVariables
  >(UPDATE_SOURCE)

  const handleSubmit = (values: Values) =>
    updateSource({
      variables: {
        sourceId: source.id,
        name: values.name,
        priority: values.priority,
      },
    })
      .then(() => enqueueSnackbar("Source updated"))
      .catch(() => {})

  return (
    <Grid container>
      <Grid item md={6} sx={{ pr: 3 }}>
        <SourceForm
          defaultValues={source}
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
        />
      </Grid>
    </Grid>
  )
}

export default UpdateSource
