import React, { useState } from "react"
import { Send } from "@mui/icons-material"
import { Box, Button, TextField } from "@mui/material"
import Form from "components/form/Form"

type ChatInputProps = {
  onInput: (message: string) => void
}

const ChatInput: React.FC<ChatInputProps> = ({ onInput }) => {
  const [value, setValue] = useState<string>("")

  const handleSubmit = () => {
    onInput(value)
    setValue("")
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if ( event.key === 'Enter' && event.shiftKey ) {
      const new_value =
      setValue(value + "\n")
      event.preventDefault()
    } else if (event.key === "Enter") {
      event.preventDefault();
      handleSubmit()
    }
  }

  return (
    <Form onSubmit={handleSubmit}>
      <Box sx={{ display: "flex", pt: 1, alignItems: "flex-end" }}>
        <TextField
          value={value}
          onChange={event => setValue(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message"
          fullWidth
          multiline
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
