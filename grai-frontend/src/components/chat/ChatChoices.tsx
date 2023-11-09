import React from "react"
import { Button, Grid } from "@mui/material"

type ChatChoicesProps = {
  choices: string[]
  onInput: (message: string) => void
}

const ChatChoices: React.FC<ChatChoicesProps> = ({ choices, onInput }) => (
  <Grid container spacing={2} sx={{ mb: 2 }}>
    <Grid item xs={1} />
    <Grid item xs={10}>
      {choices.map(choice => (
        <Button
          key={choice}
          variant="contained"
          onClick={() => onInput(choice)}
          sx={{ mb: 2, borderRadius: 4 }}
        >
          {choice}
        </Button>
      ))}
    </Grid>
  </Grid>
)

export default ChatChoices
