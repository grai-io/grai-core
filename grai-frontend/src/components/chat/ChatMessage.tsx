import React from "react"
import { Avatar, Box, Grid, Typography } from "@mui/material"
import theme from "theme"
import { GraiIconSmall } from "components/icons"

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
    <Grid container spacing={2} sx={{ mb: 2 }}>
      {side === "left" && (
        <Grid
          item
          sx={{
            display: "flex",
            justifyContent: "flex-end",
            flexDirection: "column",
          }}
        >
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
        </Grid>
      )}
      <Grid item xs={11}>
        {messages.map((msg, i) => (
          <Box
            key={i}
            sx={{
              textAlign: side === "right" ? "right" : "left",
            }}
          >
            <Typography
              align={"left"}
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
              {msg}
            </Typography>
          </Box>
        ))}
      </Grid>
      {side === "right" && (
        <Grid
          item
          sx={{
            display: "flex",
            justifyContent: "flex-end",
            flexDirection: "column",
          }}
        >
          <Avatar />
        </Grid>
      )}
    </Grid>
  )
}

export default ChatMessage
