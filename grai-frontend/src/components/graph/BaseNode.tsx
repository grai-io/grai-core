import React from "react"
import { Box, Menu, MenuItem, lighten } from "@mui/material"
import { Handle, useStore, Position, ReactFlowState } from "reactflow"
import theme from "theme"
import useWorkspace from "helpers/useWorkspace"
import BaseNodeContent from "./BaseNodeContent"
import HiddenTableButton from "./HiddenTableButton"
import Placeholder from "./Placeholder"

const zoomSelector = (s: ReactFlowState) => s.transform[2] >= 0.35
interface Column {
  id: string
  display_name: string
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
  const showContent = useStore(zoomSelector)
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
    ? theme.palette.secondary.main
    : data.searchDim
    ? "#999"
    : "rgba(0, 0, 0, 0.08)"

  const backgroundColor = data.searchHighlight
    ? lighten(theme.palette.info.light, 0.5)
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
        onDoubleClick={() => workspaceNavigate(`tables/${data.id}`)}
        sx={{
          fontSize: 12,
          borderWidth: 1,
          borderStyle: "solid",
          borderRadius: "12px",
          boxShadow: "0px 8px 20px rgba(0, 0, 0, 0.06)",
          borderColor,
          minWidth: 300,
          minHeight: 68,
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
            left: 0,
            border: 0,
            backgroundColor: "transparent",
            color: "transparent",
          }}
          isConnectable={false}
        />

        {data.hiddenDestinationTables.length > 0 && (
          <HiddenTableButton position="left" onClick={handleShowDestinations} />
        )}
        {data.hiddenSourceTables.length > 0 && (
          <HiddenTableButton position="right" onClick={handleShowSources} />
        )}
        {showContent ? <BaseNodeContent data={data} /> : <Placeholder />}
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
