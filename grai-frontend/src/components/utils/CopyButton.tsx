import React, { useState } from "react"
import { Check, ContentCopy } from "@mui/icons-material"
import { IconButton } from "@mui/material"

type CopyButtonProps = {
  text: string
}

const CopyButton: React.FC<CopyButtonProps> = ({ text }) => {
  const [done, setDone] = useState(false)

  if (done) return <Check color="success" fontSize="small" />

  const handleClick = () => {
    navigator.clipboard.writeText(text)
    setDone(true)
  }

  return (
    <IconButton size="small" sx={{ ml: 1 }} onClick={handleClick}>
      <ContentCopy fontSize="small" />
    </IconButton>
  )
}

export default CopyButton
