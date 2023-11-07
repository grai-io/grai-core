import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Grid } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import WebsocketChat from "components/chat/WebsocketChat"
import Loading from "components/layout/Loading"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceChat,
  GetWorkspaceChatVariables,
} from "./__generated__/GetWorkspaceChat"
import NotFound from "./NotFound"

export const GET_WORKSPACE = gql`
  query GetWorkspaceChat($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      last_chat {
        id
        messages {
          data {
            id
            message
            role
            created_at
          }
        }
      }
    }
  }
`

const Chat: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceChat,
    GetWorkspaceChatVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <>
      <PageHeader title="GrAI Chat" />
      <Grid container sx={{ height: "calc(100vh - 144px)" }}>
        <Grid item md={6}>
          <PageContent sx={{ height: "100%" }}>
            <WebsocketChat
              workspace={workspace}
              chat={data.workspace.last_chat}
            />
          </PageContent>
        </Grid>
      </Grid>
    </>
  )
}

export default Chat
