import React from "react"
import { ContentCopy, KeyboardBackspace } from "@mui/icons-material"
import {
  Box,
  Button,
  Divider,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"

interface Table {
  id: string
  display_name: string
}

type TableHeaderProps = {
  table: Table
}

const TableHeader: React.FC<TableHeaderProps> = ({ table }) => {
  const { routePrefix } = useWorkspace()

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={`${routePrefix}/tables`}
            color="secondary"
            startIcon={<KeyboardBackspace />}
          >
            Back
          </Button>
        </Box>
        <Typography
          variant="h6"
          sx={{ textTransform: "uppercase", mx: 1, mt: 0.3 }}
        >
          {table?.display_name ?? table?.id}
        </Typography>
        <Box>
          <Tooltip title="Copy Table Name">
            <IconButton sx={{ mt: 0.5 }}>
              <ContentCopy sx={{ fontSize: 15 }} />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      <Divider />
    </>
  )
}

export default TableHeader
