import { Box, Grid, Typography } from "@mui/material"
import ChatWindow from "components/chat/ChatWindow"
import React from "react"

const Chat: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h6">GrAI Workspace Chat</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <ChatWindow />
        </Grid>
      </Grid>
    </Box>
  )
}

export default Chat
