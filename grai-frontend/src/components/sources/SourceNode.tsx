import React, { memo, useState } from "react"
import { BarChart, Edit } from "@mui/icons-material"
import { Box, IconButton, Tooltip, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import { Handle, Position } from "reactflow"
import DataSourceIcon from "components/graph/DataSourceIcon"

type SourceNodeProps = {
  data: {
    id: string
    label: string
    icon: string | null
  }
}

const SourceNode: React.FC<SourceNodeProps> = memo(({ data }) => {
  const [hover, setHover] = useState(false)

  return (
    <Box
      sx={{
        fontSize: 12,
        borderWidth: 1,
        borderStyle: "solid",
        borderRadius: "12px",
        boxShadow: "0px 8px 20px rgba(0, 0, 0, 0.06)",
        borderColor: "rgba(0, 0, 0, 0.08)",
        minWidth: 300,
        minHeight: 68,
        cursor: "auto",
        // backgroundColor,
        // color,
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <Handle
        type="target"
        position={Position.Left}
        isConnectable={false}
        style={{
          left: 0,
          border: 0,
          backgroundColor: "transparent",
          color: "transparent",
        }}
      />
      <Box sx={{ display: "flex" }}>
        {data.icon && <DataSourceIcon dataSource={data.icon} />}
        <Box sx={{ flexGrow: 1 }}>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 600,
              fontSize: "16px",
              lineHeight: "150%",
              mt: "12px",
              mr: "12px",
            }}
          >
            {data.label}
          </Typography>
        </Box>
        {hover && (
          <Box sx={{ p: 1, pl: 0 }}>
            <Tooltip title="Edit Source">
              <IconButton component={Link} to={`sources/${data.id}`}>
                <Edit />
              </IconButton>
            </Tooltip>
            <Tooltip title="Lineage">
              <IconButton
                component={Link}
                to={`sources/${data.id}?tab=lineage`}
              >
                <BarChart />
              </IconButton>
            </Tooltip>
          </Box>
        )}
      </Box>
      <Handle
        type="source"
        position={Position.Right}
        style={{
          right: 0,
          border: 0,
          backgroundColor: "transparent",
          color: "transparent",
        }}
        isConnectable={false}
      />
    </Box>
  )
})

export default SourceNode
