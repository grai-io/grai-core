import { Box, Typography } from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import { Handle, Position } from "reactflow"
import theme from "../../theme"

interface BaseNodeProps {
  data: any
}

const BaseNode: React.FC<BaseNodeProps> = ({ data }) => {
  const navigate = useNavigate()

  const nodeType = data.metadata.node_type

  return (
    <Box
      onClick={() => navigate(`/nodes/${data.id}`)}
      sx={{
        fontSize: 12,
        borderWidth: 1,
        borderStyle: "solid",
        borderRadius: nodeType === "Table" ? "25px" : "3px",
        borderColor: data.highlight
          ? theme.palette.primary.contrastText
          : "#555",
        textAlign: "center",
        width: 250,
        p: "10px",
        cursor: "pointer",
      }}
    >
      <Handle
        type="target"
        position={"top" as Position}
        style={{
          top: -2,
          border: 0,
          backgroundColor: "transparent",
          color: "transparent",
        }}
        onConnect={params => console.log("handle onConnect", params)}
        isConnectable={false}
      />
      <Typography variant="h6">{data.label}</Typography>
      {Object.entries(data.metadata)
        .filter(([key, value]) => value)
        .map(([key, value]) => (
          <React.Fragment key={key}>
            <Typography
              variant="caption"
              sx={{ display: "block" }}
            >{`${key}: ${value}`}</Typography>
          </React.Fragment>
        ))}
      <Handle
        type="source"
        position={"bottom" as Position}
        style={{
          bottom: 0,
          border: 0,
          backgroundColor: "transparent",
          color: "transparent",
        }}
        isConnectable={false}
      />
    </Box>
  )
}

export default BaseNode
