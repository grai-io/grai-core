import { Send } from "@mui/icons-material"
import { Box, Button, TextField } from "@mui/material"
import Form from "components/form/Form"
import React, { useState } from "react"

type ChatInputProps = {
  onInput: (message: string) => void
}

const ChatInput: React.FC<ChatInputProps> = ({ onInput }) => {
  const [value, setValue] = useState<string>("")

  const handleSubmit = () => {
    onInput(value)
    setValue("")
  }

  return (
    <Form onSubmit={handleSubmit}>
      <Box sx={{ display: "flex", pt: 3 }}>
        <TextField
          value={value}
          onChange={event => setValue(event.target.value)}
          placeholder="Type a message"
          fullWidth
          sx={{ flexGrow: 1 }}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={!value}
          sx={{ ml: 2 }}
        >
          <Send />
        </Button>
      </Box>
    </Form>
  )
}

export default ChatInput
