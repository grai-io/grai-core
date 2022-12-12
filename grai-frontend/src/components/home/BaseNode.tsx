import { ArrowDropDown } from "@mui/icons-material"
import { Box, Divider, Menu, MenuItem, Typography } from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import { Handle, Position } from "reactflow"
import theme from "../../theme"

interface BaseNodeProps {
  data: {
    id: string
    label: string
    highlight: boolean
    count: number
  }
}

const BaseNode: React.FC<BaseNodeProps> = ({ data }) => {
  const navigate = useNavigate()
  const [contextMenu, setContextMenu] = React.useState<{
    mouseX: number
    mouseY: number
  } | null>(null)

  const handleContextMenu = (event: React.MouseEvent) => {
    event.preventDefault()
    setContextMenu(
      contextMenu === null
        ? {
            mouseX: event.clientX + 2,
            mouseY: event.clientY - 6,
          }
        : // repeated contextmenu when it is already open closes it with Chrome 84 on Ubuntu
          // Other native context menus might behave different.
          // With this behavior we prevent contextmenu from the backdrop to re-locale existing context menus.
          null
    )
  }

  const handleClose = () => {
    setContextMenu(null)
  }

  return (
    <>
      <Box
        onContextMenu={handleContextMenu}
        sx={{
          fontSize: 12,
          borderWidth: 1,
          borderStyle: "solid",
          borderRadius: 1,
          borderColor: data.highlight
            ? theme.palette.primary.contrastText
            : "#555",
          minWidth: 300,
          p: "10px",
          py: "5px",
          cursor: "auto",
          backgroundColor: "white",
        }}
      >
        <Handle
          type="target"
          position={"left" as Position}
          style={{
            left: -2,
            border: 0,
            backgroundColor: "transparent",
            color: "transparent",
          }}
          isConnectable={false}
        />
        <Typography variant="h6">{data.label}</Typography>
        {data.count > 0 && (
          <>
            <Divider sx={{ mt: 0.5, mb: 1 }} />
            <Box sx={{ display: "flex" }}>
              <Typography sx={{ flexGrow: 1 }}>
                {data.count} Column{data.count > 1 && "s"}
              </Typography>
              <Box
                sx={{ cursor: "pointer" }}
                onClick={() => console.log("click")}
              >
                <ArrowDropDown />
              </Box>
            </Box>
          </>
        )}
        <Handle
          type="source"
          position={"right" as Position}
          style={{
            right: 0,
            border: 0,
            backgroundColor: "transparent",
            color: "transparent",
          }}
          isConnectable={false}
        />
      </Box>
      <Menu
        open={contextMenu !== null}
        onClose={handleClose}
        anchorReference="anchorPosition"
        anchorPosition={
          contextMenu !== null
            ? { top: contextMenu.mouseY, left: contextMenu.mouseX }
            : undefined
        }
      >
        <MenuItem onClick={handleClose}>
          Show lineage for <b>{data.label}</b>
        </MenuItem>
        <MenuItem onClick={handleClose}>Show upstream dependents</MenuItem>
        <MenuItem onClick={handleClose}>Show downstream dependents</MenuItem>
        <MenuItem onClick={() => navigate(`/nodes/${data.id}`)}>
          Show profile for this table
        </MenuItem>
      </Menu>
    </>
  )
}

export default BaseNode
