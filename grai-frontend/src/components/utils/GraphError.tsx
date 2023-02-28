import React from "react"
import { ApolloError } from "@apollo/client"
import { Alert, AlertTitle } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Navigate } from "react-router-dom"

type GraphErrorProps = {
  error: ApolloError
}

const GraphError: React.FC<GraphErrorProps> = ({ error }) => {
  const { organisationName, workspaceName } = useWorkspace()

  if (error.message === "Can't find workspace") {
    return (
      <Navigate
        to="/workspaces"
        state={{
          workspaceNotFound: true,
          organisationName,
          workspaceName,
        }}
      />
    )
  }

  return (
    <Alert severity="error">
      <AlertTitle>Error</AlertTitle>
      {error.message}
    </Alert>
  )
}

export default GraphError
