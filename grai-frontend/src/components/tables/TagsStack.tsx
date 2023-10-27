import React from "react"
import { Chip, Stack } from "@mui/material"

type TagsStackProps = {
  tags?: string[]
}

const TagsStack: React.FC<TagsStackProps> = ({ tags }) =>
  tags ? (
    <Stack direction="row" spacing={1}>
      {tags.map((tag: string) => (
        <Chip label={tag} key={tag} />
      ))}
    </Stack>
  ) : null

export default TagsStack
