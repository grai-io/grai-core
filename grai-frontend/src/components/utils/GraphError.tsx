import React from "react"
import { ApolloError } from "@apollo/client"
import { Alert, AlertTitle, Stack, Typography } from "@mui/material"
import { Navigate } from "react-router-dom"
import arrayWrap from "helpers/arrayWrap"
import useWorkspace from "helpers/useWorkspace"

const parseJsonError = (error: ApolloError) => {
  try {
    return JSON.parse(error.message)
  } catch (e) {
    return error.message
  }
}

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
      <Stack spacing={1}>
        {arrayWrap(parseJsonError(error)).map((message: string) => (
          <Typography variant="body2">{message}</Typography>
        ))}
      </Stack>
    </Alert>
  )
}

export default GraphError
