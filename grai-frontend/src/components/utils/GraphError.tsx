import React from "react"
import { ApolloError } from "@apollo/client"
import { Typography } from "@mui/material"

type GraphErrorProps = {
  error: ApolloError
}

export default function GraphError(props: GraphErrorProps) {
  const { error } = props

  return (
    <Typography variant="body1" color="error">
      {error.message}
    </Typography>
  )
}
