import React from "react"
import { Avatar, Box } from "@mui/material"
import Typography from "@mui/material/Typography"
import theme from "theme"
import { GraiIconSmall } from "components/icons"
import Markdown from "components/utils/Markdown"

export type GroupedChats = {
  sender: boolean
  messages: string[]
}

const radius = theme.spacing(2.5)
const rightBgColor = "rgba(131, 56, 236)"

const classes = {
  agent: {
    borderTopRightRadius: radius,
    borderBottomRightRadius: radius,
  },
  user: {
    borderTopRightRadius: radius,
    borderBottomRightRadius: radius,
  },
}

type MessageComponentProps = {
  sender: "agent" | "user"
  message: string
}

const MessageComponent: React.FC<MessageComponentProps> = ({
  sender,
  message,
}) => (
  <Box>
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
      }}
    >
      <Box>
        {sender === "agent" ? (
          <Avatar
            sx={{
              backgroundColor: "white",
              borderColor: rightBgColor,
              borderWidth: 2,
              borderStyle: "solid",
            }}
          >
            <GraiIconSmall />
          </Avatar>
        ) : (
          <Avatar />
        )}
      </Box>
      <Box sx={{ px: 2 }}>
        <Typography
          sx={{
            fontWeight: "bold",
          }}
        >
          {sender === "agent" ? "Grai" : "You"}
        </Typography>
        <Box
          sx={{
            mb: 0.5,
            display: "inline-block",
            wordBreak: "break-word",
            fontFamily:
              // eslint-disable-next-line max-len
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
            fontSize: "14px",
            borderRadius: 1,
            ...classes[sender],
          }}
        >
          <Markdown message={message} />
        </Box>
      </Box>
    </Box>
  </Box>
)

type ChatMessageProps = {
  groupedChat: GroupedChats
}

const ChatMessage: React.FC<ChatMessageProps> = ({ groupedChat }) => {
  const sender = groupedChat.sender ? "user" : "agent"
  const messages = groupedChat.messages

  return (
    <Box sx={{ display: "flex", mb: 2 }}>
      <Box sx={{ width: "100%" }}>
        {messages.map((msg, i) => (
          <Box key={i}>
            <MessageComponent sender={sender} message={msg} />
          </Box>
        ))}
      </Box>
    </Box>
  )
}

export default ChatMessage
