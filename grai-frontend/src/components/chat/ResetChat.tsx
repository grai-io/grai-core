import React from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box } from "@mui/material"
import { useSnackbar } from "notistack"
import { CreateChat, CreateChatVariables } from "./__generated__/CreateChat"

export const CREATE_CHAT = gql`
  mutation CreateChat($workspaceId: ID!) {
    createChat(workspaceId: $workspaceId) {
      id
    }
  }
`

type ResetChatProps = {
  workspaceId: string
}

const ResetChat: React.FC<ResetChatProps> = ({ workspaceId }) => {
  const { enqueueSnackbar } = useSnackbar()

  const [createChat, { loading }] = useMutation<
    CreateChat,
    CreateChatVariables
  >(CREATE_CHAT, {
    variables: {
      workspaceId,
    },
  })

  const handleClick = () => {
    createChat()
      .then(() => enqueueSnackbar("Chat restarted"))
      .catch(() =>
        enqueueSnackbar("Failed to restart chat", { variant: "error" }),
      )
  }

  return (
    <Box>
      <LoadingButton
        onClick={handleClick}
        loading={loading}
        sx={{ color: "gray" }}
      >
        Restart chat
      </LoadingButton>
    </Box>
  )
}

export default ResetChat
