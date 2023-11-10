import React from "react"
import { Grid } from "@mui/material"
import WebsocketChat from "components/chat/WebsocketChat"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"

const Chat: React.FC = () => (
  <>
    <PageHeader title="GrAI Chat" />
    <Grid container sx={{ height: "calc(100vh - 144px)" }}>
      <Grid item md={6}>
        <PageContent sx={{ height: "100%" }}>
          <WebsocketChat />
        </PageContent>
      </Grid>
    </Grid>
  </>
)

export default Chat
