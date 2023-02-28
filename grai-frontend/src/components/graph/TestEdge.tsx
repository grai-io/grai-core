import React, { useState } from "react"
import { CheckCircleOutline, ErrorOutline } from "@mui/icons-material"
import {
  Alert,
  AlertTitle,
  Box,
  Divider,
  Stack,
  Typography,
} from "@mui/material"
import { EdgeProps, getBezierPath, EdgeLabelRenderer } from "reactflow"
import theme from "theme"

interface Test {
  message: string
  test_pass?: boolean
}

export type TestData = {
  tests?: Test[]
}

const TestEdge: React.FC<EdgeProps<TestData>> = ({
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

  const errorCount = data?.tests?.filter(test => !test.test_pass).length
  const passCount = data?.tests?.filter(test => test.test_pass).length

  const hasError = errorCount ? errorCount > 0 : false
  const hasPass = passCount ? passCount > 0 : false

  return (
    <>
      <path
        id={id}
        className="react-flow__edge-path"
        d={edgePath}
        style={{
          stroke: hasError ? theme.palette.error.main : undefined,
        }}
      />
      <EdgeLabelRenderer>
        <Alert
          severity={hasError ? "error" : "success"}
          icon={false}
          onClick={toggleExpand}
          sx={{
            pointerEvents: "all",
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            zIndex: 20,
            width: expand ? 225 : undefined,
            overflowWrap: "break-word",
          }}
          className="nodrag nopan"
          data-testid="test-edge"
        >
          <Box sx={{ display: "flex" }}>
            {hasError && (
              <>
                <ErrorOutline sx={{ mr: 1 }} />
                <AlertTitle sx={{ mt: 0.1 }}>{errorCount}</AlertTitle>
              </>
            )}
            {hasPass && (
              <>
                <CheckCircleOutline sx={{ mr: 1 }} />
                <AlertTitle sx={{ mt: 0.1 }}>{passCount}</AlertTitle>
              </>
            )}
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
                {data?.tests?.map((test, index) => (
                  <Typography variant="body2" key={index}>
                    {test.message}
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

export default TestEdge
