import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Button, Tooltip } from "@mui/material"
import { Field, Filter } from "components/filters/filters"
import AddPopper from "./AddPopper"

type AddButtonProps = {
  fields: Field[]
  onAdd: (newFilter: Filter) => void
}

const AddButton: React.FC<AddButtonProps> = ({ fields, onAdd }) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const handleClick = (event: React.MouseEvent<HTMLElement>) =>
    setAnchorEl(event.currentTarget)

  return (
    <>
      <Tooltip title="Add Filter Row">
        <Button
          variant="outlined"
          onClick={handleClick}
          fullWidth
          sx={{ borderRadius: 24, mt: 2 }}
        >
          <Add />
        </Button>
      </Tooltip>
      <AddPopper
        anchorEl={anchorEl}
        setAnchorEl={setAnchorEl}
        fields={fields}
        onAdd={onAdd}
      />
    </>
  )
}

export default AddButton
