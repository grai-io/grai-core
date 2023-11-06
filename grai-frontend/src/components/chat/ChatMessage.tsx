import React from "react"
import { Avatar, Box, Grid, Typography } from "@mui/material"
import theme from "theme"
import { GraiIconSmall } from "components/icons"
import { Chat } from "./ChatWindow"

const radius = theme.spacing(2.5)
const rightBgColor = "rgba(131, 56, 236)"

const classes = {
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
  chat: Chat
}

const ChatMessage: React.FC<ChatMessageProps> = ({ chat }) => {
  const side = chat.sender ? "right" : "left"

  const messages = [chat.message]

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
    <Grid container spacing={2}>
      {side === "left" && (
        <Grid item>
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
              ...attachClass(i),
              textAlign: side === "right" ? "right" : "left",
            }}
          >
            <Typography
              align={"left"}
              sx={{
                bgcolor: side === "right" ? rightBgColor : "grey.200",
                color: side === "right" ? "white" : "black",
                borderRadius: radius,
                padding: theme.spacing(1),
                marginBottom: 4,
                display: "inline-block",
                wordBreak: "break-word",
                fontFamily:
                  // eslint-disable-next-line max-len
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
                fontSize: "14px",
                px: 2,
              }}
            >
              {msg}
            </Typography>
          </Box>
        ))}
      </Grid>
      {side === "right" && (
        <Grid item>
          <Avatar />
        </Grid>
      )}
    </Grid>
  )
}

export default ChatMessage
