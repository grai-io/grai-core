import { ErrorOutline } from "@mui/icons-material"
import {
  Alert,
  AlertTitle,
  Box,
  Divider,
  Stack,
  Typography,
} from "@mui/material"
import React, { useState } from "react"
import { EdgeProps, getBezierPath, EdgeLabelRenderer } from "reactflow"

interface Error {
  message: string
}

export type ErrorData = {
  errors?: Error[]
}

const ErrorEdge: React.FC<EdgeProps<ErrorData>> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
}) => {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  })

  const [expand, setExpand] = useState(false)

  const toggleExpand = () => setExpand(!expand)

  return (
    <>
      <path id={id} className="react-flow__edge-path" d={edgePath} />
      <EdgeLabelRenderer>
        <Alert
          severity="error"
          icon={false}
          onClick={toggleExpand}
          sx={{
            pointerEvents: "all",
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            zIndex: 20,
            width: 225,
            overflowWrap: "break-word",
          }}
          className="nodrag nopan"
        >
          <Box sx={{ display: "flex" }}>
            <ErrorOutline sx={{ mr: 1 }} />
            <AlertTitle sx={{ mt: 0.1 }}>Errors</AlertTitle>
          </Box>
          {expand && (
            <>
              <Divider
                sx={{
                  mt: 0.5,
                  mb: 1,
                  borderColor: "rgba(95, 33, 32, 0.25)",
                }}
              />
              <Stack spacing={1}>
                {data?.errors?.map((error, index) => (
                  <Typography variant="body2" key={index}>
                    {error.message}
                  </Typography>
                ))}
              </Stack>
            </>
          )}
        </Alert>
      </EdgeLabelRenderer>
    </>
  )
}

export default ErrorEdge
