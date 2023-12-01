import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Grid } from "@mui/material"
import { useSnackbar } from "notistack"
import NotFound from "pages/NotFound"
import useSearchParams from "helpers/useSearchParams"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import PageContent from "components/layout/PageContent"
import GraphError from "components/utils/GraphError"
import {
  GetConnectionSchedule,
  GetConnectionScheduleVariables,
} from "./__generated__/GetConnectionSchedule"
import ConnectionToolbar from "./ConnectionToolbar"
import ScheduleForm from "./ScheduleForm"
import ScheduleHelp from "../schedule/ScheduleHelp"

export const GET_CONNECTION = gql`
  query GetConnectionSchedule($workspaceId: ID!, $connectionId: ID!) {
    workspace(id: $workspaceId) {
      id
      connection(id: $connectionId) {
        id
        name
        connector {
          id
          slug
          name
          icon
          metadata
        }
        metadata
      }
    }
  }
`

type ScheduleTabProps = {
  workspaceId: string
  connectionId: string
}

const ScheduleTab: React.FC<ScheduleTabProps> = ({
  workspaceId,
  connectionId,
}) => {
  const { workspaceNavigate } = useWorkspace()
  const { setSearchParam } = useSearchParams()
  const { enqueueSnackbar } = useSnackbar()

  const { loading, error, data } = useQuery<
    GetConnectionSchedule,
    GetConnectionScheduleVariables
  >(GET_CONNECTION, {
    variables: {
      workspaceId,
      connectionId,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const connection = data?.workspace?.connection

  if (!connection) return <NotFound />

  const handleComplete = () => {
    enqueueSnackbar("Connection successfully created", {
      variant: "success",
    })
    workspaceNavigate(`connections/${connection.id}`)
  }
  const handleBack = () => setSearchParam("step", null)

  return (
    <>
      <PageContent noPadding>
        <ConnectionToolbar
          title="Set Schedule"
          activeStep={2}
          onBack={handleBack}
        />
      </PageContent>
      <Grid container>
        <Grid item md={6}>
          <PageContent>
            <ScheduleForm connection={connection} onComplete={handleComplete} />
          </PageContent>
        </Grid>
        <Grid item md={6}>
          <PageContent>
            <ScheduleHelp />
          </PageContent>
        </Grid>
      </Grid>
    </>
  )
}

export default ScheduleTab
