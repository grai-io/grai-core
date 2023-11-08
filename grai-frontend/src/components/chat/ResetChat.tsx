import React from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box } from "@mui/material"
import { useSnackbar } from "notistack"
import { CreateChat, CreateChatVariables } from "./__generated__/CreateChat"
import { NewChat } from "./__generated__/NewChat"

export const CREATE_CHAT = gql`
  mutation CreateChat($workspaceId: ID!) {
    createChat(workspaceId: $workspaceId) {
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
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          /* istanbul ignore next */
          last_chat(existingChat) {
            if (!data?.createChat) return existingChat

            const newChat = cache.writeFragment<NewChat>({
              data: data?.createChat,
              fragment: gql`
                fragment NewChat on Chat {
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
              `,
            })

            return newChat
          },
        },
      })
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
