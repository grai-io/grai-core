import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Button } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import AddSourceDialog from "./AddSourceDialog"

interface Organisation {
  id: string
}

interface Workspace {
  id: string
  sample_data: boolean
  organisation: Organisation
}

type AddSourceButtonProps = {
  workspace: Workspace
}

const AddSourceButton: React.FC<AddSourceButtonProps> = ({ workspace }) => {
  const { routePrefix } = useWorkspace()

  const [show, setShow] = useState(false)

  const defaultProps = {
    startIcon: <Add />,
    sx: {
      backgroundColor: "#FC6016",
      boxShadow: "0px 4px 6px rgba(252, 96, 22, 0.2)",
      borderRadius: "8px",
      height: "40px",
    },
  }

  if (workspace.sample_data) {
    const handleClick = () => setShow(true)

    return (
      <>
        <Button variant="contained" {...defaultProps} onClick={handleClick}>
          Add Source
        </Button>
        {show && (
          <AddSourceDialog
            open={show}
            onClose={() => setShow(false)}
            organisationId={workspace.organisation.id}
          />
        )}
      </>
    )
  }

  return (
    <Button
      variant="contained"
      component={Link}
      to={`${routePrefix}/connections/create`}
      {...defaultProps}
    >
      Add Source
    </Button>
  )
}

export default AddSourceButton
