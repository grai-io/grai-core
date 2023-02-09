import { gql, useMutation } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { useSnackbar } from "notistack"
import React, { useEffect } from "react"
import { Navigate, useSearchParams } from "react-router-dom"
import {
  AddInstallation,
  AddInstallationVariables,
} from "./__generated__/AddInstallation"

export const ADD_INSTALLATION = gql`
  mutation AddInstallation($installationId: Int!) {
    addInstallation(installationId: $installationId) {
      success
    }
  }
`

const PostInstall: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar()
  const [searchParams] = useSearchParams()

  const [addInstallation, { data, error }] = useMutation<
    AddInstallation,
    AddInstallationVariables
  >(ADD_INSTALLATION, {
    variables: {
      installationId: Number(searchParams.get("installation_id")),
    },
  })

  useEffect(() => {
    addInstallation().then(() => enqueueSnackbar("Github updated"))
  }, [addInstallation, enqueueSnackbar])

  if (error) return <GraphError error={error} />
  if (data) return <Navigate to="/" />

  return <Loading />
}

export default PostInstall
