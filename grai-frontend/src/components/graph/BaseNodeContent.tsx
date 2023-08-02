import React from "react"
import { ExpandLess, ExpandMore } from "@mui/icons-material"
import { Box, Typography, Stack } from "@mui/material"
import { Handle, Position } from "reactflow"
import { BaseNodeData } from "./BaseNode"
import DataSourceIcon from "./DataSourceIcon"

type BaseNodeContentProps = {
  data: BaseNodeData
}

const BaseNodeContent: React.FC<BaseNodeContentProps> = ({ data }) => (
  <>
    <Box sx={{ display: "flex" }}>
      {data.data_source && <DataSourceIcon dataSource={data.data_source} />}
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
        <Typography
          sx={{
            fontWeight: 400,
            fontSize: "12px",
            lineHeight: "150%",
            mt: "2px",
          }}
        >
          {data.columns.length > 0 &&
            `${data.columns.length} Column${data.columns.length > 1 && "s"}`}
        </Typography>
      </Box>
      {data.columns.length > 0 && (
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            mr: "12px",
            color: "#8338EC",
          }}
          onClick={() => data.onExpand(!data.expanded)}
        >
          {data.expanded ? (
            <ExpandLess fontSize="large" />
          ) : (
            <ExpandMore fontSize="large" className="table-expand" />
          )}
        </Box>
      )}
    </Box>
    {data.expanded && (
      <Stack direction="column" spacing={1} sx={{ px: 1, pb: 1, mt: -0.5 }}>
        {data.columns.map((column, index) => (
          <Box
            key={column.id}
            sx={{
              border: "1px solid rgba(0, 0, 0, 0.08)",
              borderRadius: "8px",
              p: 1,
            }}
          >
            <Typography>{column.display_name}</Typography>
            <Handle
              id={column.id}
              type="target"
              position={"left" as Position}
              style={{
                top: 86 + index * 50,
                left: 10,
                border: 0,
                backgroundColor: "transparent",
                color: "transparent",
              }}
              isConnectable={false}
            />
            <Handle
              id={column.id}
              type="source"
              position={"right" as Position}
              style={{
                top: 86 + index * 50,
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
  </>
)

export default BaseNodeContent
