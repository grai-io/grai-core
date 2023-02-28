import React from "react"
import { ArrowDropDown, ArrowDropUp } from "@mui/icons-material"
import { Box, Divider, Menu, MenuItem, Stack, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Handle, Position } from "reactflow"
import theme from "theme"
import DataSourceIcon from "./DataSourceIcon"
import HiddenTableButton from "./HiddenTableButton"

interface Column {
  display_name?: string | null
  name: string
}

export type BaseNodeData = {
  id: string
  label: string
  data_source: string
  highlight: boolean
  columns: Column[]
  hiddenSourceTables: string[]
  hiddenDestinationTables: string[]
  expanded: boolean
  onExpand: (value: boolean) => void
  onShow: (values: string[]) => void
  searchHighlight: boolean
  searchDim: boolean
}

interface BaseNodeProps {
  data: BaseNodeData
}

const BaseNode: React.FC<BaseNodeProps> = ({ data }) => {
  const { workspaceNavigate } = useWorkspace()
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

  const handleShowHidden = () => {
    data.onShow([...data.hiddenSourceTables, ...data.hiddenDestinationTables])
    handleClose()
  }
  const handleShowSources = () => {
    data.onShow(data.hiddenSourceTables)
    handleClose()
  }
  const handleShowDestinations = () => {
    data.onShow(data.hiddenDestinationTables)
    handleClose()
  }

  const borderColor = data.highlight
    ? theme.palette.primary.contrastText
    : data.searchDim
    ? "#999"
    : "#555"

  const backgroundColor = data.searchHighlight
    ? theme.palette.info.light
    : "white"

  const color = data.searchDim
    ? theme.palette.grey[500]
    : data.searchHighlight
    ? theme.palette.info.contrastText
    : undefined

  return (
    <>
      <Box
        onContextMenu={handleContextMenu}
        sx={{
          fontSize: 12,
          borderWidth: 1,
          borderStyle: "solid",
          borderRadius: 1,
          borderColor,
          minWidth: 300,
          cursor: "auto",
          backgroundColor,
          color,
        }}
      >
        <Handle
          id="all"
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
        <Box sx={{ p: 2, py: 1 }}>
          {data.hiddenDestinationTables.length > 0 && (
            <HiddenTableButton
              position="left"
              onClick={handleShowDestinations}
            />
          )}
          {data.hiddenSourceTables.length > 0 && (
            <HiddenTableButton position="right" onClick={handleShowSources} />
          )}
          <Box sx={{ display: "flex" }}>
            <DataSourceIcon dataSource={data.data_source} />
            <Typography variant="h6">{data.label}</Typography>
          </Box>
          {data.columns.length > 0 && (
            <>
              <Divider sx={{ mt: 0.5, mb: 1 }} />
              <Box sx={{ display: "flex" }}>
                <Typography sx={{ flexGrow: 1 }}>
                  {data.columns.length} Column{data.columns.length > 1 && "s"}
                </Typography>
                <Box
                  sx={{ cursor: "pointer" }}
                  onClick={() => data.onExpand(!data.expanded)}
                >
                  {data.expanded ? <ArrowDropUp /> : <ArrowDropDown />}
                </Box>
              </Box>
            </>
          )}
        </Box>
        {data.expanded && (
          <Stack direction="column" spacing={1} sx={{ px: 1, pb: 1, mt: -0.5 }}>
            {data.columns.map((column, index) => (
              <Box
                key={column.name}
                sx={{
                  borderStyle: "solid",
                  borderWidth: 1,
                  borderColor: "divider",
                  borderRadius: 1,
                  p: 1,
                }}
              >
                <Typography>{column.display_name ?? column.name}</Typography>
                <Handle
                  id={column.name}
                  type="target"
                  position={"left" as Position}
                  style={{
                    top: 108 + index * 50,
                    left: 10,
                    border: 0,
                    backgroundColor: "transparent",
                    color: "transparent",
                  }}
                  isConnectable={false}
                />
                <Handle
                  id={column.name}
                  type="source"
                  position={"right" as Position}
                  style={{
                    top: 108 + index * 50,
                    right: 10,
                    border: 0,
                    backgroundColor: "transparent",
                    color: "transparent",
                  }}
                  isConnectable={false}
                />
              </Box>
            ))}
          </Stack>
        )}
        <Handle
          id="all"
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
        <MenuItem onClick={handleShowHidden}>
          Show lineage for {data.label}
        </MenuItem>
        <MenuItem
          onClick={handleShowDestinations}
          disabled={data.hiddenDestinationTables.length === 0}
        >
          Show upstream dependents
        </MenuItem>
        <MenuItem
          onClick={handleShowSources}
          disabled={data.hiddenSourceTables.length === 0}
        >
          Show downstream dependents
        </MenuItem>
        <MenuItem onClick={() => workspaceNavigate(`tables/${data.id}`)}>
          Show profile for this table
        </MenuItem>
      </Menu>
    </>
  )
}

export default BaseNode
