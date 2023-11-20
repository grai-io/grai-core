import React, { Suspense } from "react"
import { gql, useQuery } from "@apollo/client"
import { Outlet, useParams } from "react-router-dom"
import ChatProvider from "components/chat/ChatProvider"
import Loading from "components/layout/Loading"
import PageLayout from "components/layout/PageLayout"
import {
  GetWorkspaceProvider,
  GetWorkspaceProviderVariables,
} from "./__generated__/GetWorkspaceProvider"
import WorkspaceProvider from "./WorkspaceProvider"

export const GET_WORKSPACE = gql`
  query GetWorkspaceProvider(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
      sample_data
      organisation {
        id
      }
      runs(filters: { action: TESTS }) {
        meta {
          filtered
        }
      }
      nodes(filters: { node_type: { equals: "Table" } }) {
        meta {
          filtered
        }
      }
      connections {
        meta {
          total
        }
      }
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
    profile {
      id
      username
      first_name
      last_name
    }
  }
`

const WorkspaceOutlet: React.FC = () => {
  const { organisationName, workspaceName } = useParams()

  const { data } = useQuery<
    GetWorkspaceProvider,
    GetWorkspaceProviderVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName: organisationName ?? "",
      workspaceName: workspaceName ?? "",
    },
  })

  const gettingStarted =
    data && (data?.workspace.connections.meta.total ?? 0) === 0
  const sampleData = data?.workspace.sample_data

  if (!data?.workspace)
    return (
      <WorkspaceProvider>
        <PageLayout
          gettingStarted={gettingStarted}
          sampleData={sampleData}
          workspace={data?.workspace}
          profile={data?.profile}
        >
          <Suspense fallback={<Loading />}>
            <Outlet />
          </Suspense>
        </PageLayout>
      </WorkspaceProvider>
    )

  return (
    <WorkspaceProvider>
      <ChatProvider workspace={data.workspace} chat={data.workspace.last_chat}>
        <PageLayout
          gettingStarted={gettingStarted}
          sampleData={sampleData}
          workspace={data?.workspace}
          profile={data?.profile}
        >
          <Suspense fallback={<Loading />}>
            <Outlet />
          </Suspense>
        </PageLayout>
      </ChatProvider>
    </WorkspaceProvider>
  )
}

export default WorkspaceOutlet
