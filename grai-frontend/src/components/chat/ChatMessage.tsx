import React from "react"
import { Avatar, Box } from "@mui/material"
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
  left: {
    borderTopRightRadius: radius,
    borderBottomRightRadius: radius,
    backgroundColor: theme.palette.grey[100],
  },
  right: {
    borderTopLeftRadius: radius,
    borderBottomLeftRadius: radius,
    backgroundColor: rightBgColor,
    color: theme.palette.common.white,
  },
  leftFirst: {
    borderTopLeftRadius: radius,
  },
  leftLast: {
    borderBottomLeftRadius: radius,
  },
  rightFirst: {
    borderTopRightRadius: radius,
  },
  rightLast: {
    borderBottomRightRadius: radius,
  },
}

type ChatMessageProps = {
  groupedChat: GroupedChats
}

const ChatMessage: React.FC<ChatMessageProps> = ({ groupedChat }) => {
  const side = groupedChat.sender ? "right" : "left"

  const messages = groupedChat.messages

  const attachClass = (index: number) => {
    if (index === 0) {
      return classes[`${side}First`]
    }
    if (index === messages.length - 1) {
      return classes[`${side}Last`]
    }
    return ""
  }

  return (
    <Box sx={{ display: "flex", mb: 2 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-end",
          flexDirection: "column",
          width: "48px",
          mr: 1,
        }}
      >
        <Box>
          {side === "left" && (
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
          )}
        </Box>
      </Box>

      <Box sx={{ width: "100%" }}>
        {messages.map((msg, i) => (
          <Box
            key={i}
            sx={{
              textAlign: side === "right" ? "right" : "left",
            }}
          >
            <Box
              sx={{
                px: 2,
                py: 1,
                mb: 0.5,
                display: "inline-block",
                wordBreak: "break-word",
                fontFamily:
                  // eslint-disable-next-line max-len
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
                fontSize: "14px",
                borderRadius: 1,
                ...attachClass(i),
                ...classes[side],
              }}
            >
              <Markdown message={msg} />
            </Box>
          </Box>
        ))}
      </Box>

      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-end",
          flexDirection: "column",
          width: "48px",
          ml: 1,
        }}
      >
        {side === "right" && <Avatar />}
      </Box>
    </Box>
  )
}

export default ChatMessage
