import React from "react"
import { ApolloError } from "@apollo/client"
import { Alert, AlertTitle } from "@mui/material"

type GraphErrorProps = {
  error: ApolloError
}

export default function GraphError(props: GraphErrorProps) {
  const { error } = props

  return (
    <Alert severity="error">
      <AlertTitle>Error</AlertTitle>
      {error.message}
    </Alert>
  )
}
