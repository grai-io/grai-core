import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Grid } from "@mui/material"
import { useSnackbar } from "notistack"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import {
  CreateSource as CreateSourceType,
  CreateSourceVariables,
} from "./__generated__/CreateSource"
import { NewSource } from "./__generated__/NewSource"
import SourceForm, { Values } from "./SourceForm"

export const CREATE_SOURCE = gql`
  mutation CreateSource($workspaceId: ID!, $name: String!, $priority: Int!) {
    createSource(workspaceId: $workspaceId, name: $name, priority: $priority) {
      id
      name
      priority
    }
  }
`

type CreateSourceProps = {
  workspaceId: string
}

const CreateSource: React.FC<CreateSourceProps> = ({ workspaceId }) => {
  const { enqueueSnackbar } = useSnackbar()
  const navigate = useNavigate()
  const { routePrefix } = useWorkspace()

  const defaultValues: Values = {
    name: "",
    priority: 0,
  }

  const [createSource, { loading, error }] = useMutation<
    CreateSourceType,
    CreateSourceVariables
  >(CREATE_SOURCE, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          sources(existingSources = { data: [] }) {
            if (!data?.createSource) return existingSources

            const newSource = cache.writeFragment<NewSource>({
              data: data.createSource,
              fragment: gql`
                fragment NewSource on Source {
                  id
                  name
                }
              `,
            })
            return {
              data: [...existingSources.data, newSource],
              meta: {
                total: (existingSources.meta?.total ?? 0) + 1,
                __typename: "SourcePagination",
              },
            }
          },
        },
      })
    },
  })

  const handleSubmit = (values: Values) =>
    createSource({
      variables: {
        workspaceId,
        name: values.name,
        priority: values.priority,
      },
    })
      .then(
        res =>
          res.data?.createSource.id &&
          navigate(`${routePrefix}/sources/${res.data.createSource.id}`),
      )
      .then(() => enqueueSnackbar("Source created"))
      .catch(() => {})

  return (
    <Grid container>
      <Grid item md={6} sx={{ pr: 3 }}>
        <SourceForm
          defaultValues={defaultValues}
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
        />
      </Grid>
    </Grid>
  )
}

export default CreateSource
