import React, { useEffect } from "react"
import { gql, useMutation } from "@apollo/client"
import { useNavigate, useSearchParams } from "react-router-dom"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { Verify, VerifyVariables } from "./__generated__/Verify"
import { useSnackbar } from "notistack"

export const VERIFY_EMAIL = gql`
  mutation Verify($uid: String!, $token: String!) {
    verifyEmail(uid: $uid, token: $token) {
      id
    }
  }
`

const VerifyEmail: React.FC = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { enqueueSnackbar } = useSnackbar()

  const [verifyEmail, { error }] = useMutation<Verify, VerifyVariables>(
    VERIFY_EMAIL,
  )

  const uid = searchParams.get("uid")
  const token = searchParams.get("token")

  useEffect(() => {
    if (!uid || !token) return

    verifyEmail({
      variables: {
        uid,
        token,
      },
    })
      .then(() => enqueueSnackbar("Email verified", { variant: "success" }))
      .then(() => {
        navigate("/")
      })
      .catch(() => {})
  }, [uid, token, verifyEmail, navigate])

  if (error) return <GraphError error={error} />

  if (!uid || !token) return <>Missing required token</>

  return <Loading />
}

export default VerifyEmail
