import React, { useState } from "react"
import { CancelOutlined, CheckCircleOutline } from "@mui/icons-material"
import { Box, Card, CardContent, lighten } from "@mui/material"
import { EdgeProps, getBezierPath, EdgeLabelRenderer } from "reactflow"
import theme from "theme"
import TestSection from "./tests/TestSection"
import TestsSummary from "./tests/TestsSummary"

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

  const errorCount = data?.tests?.filter(test => !test.test_pass).length ?? 0
  const passCount = data?.tests?.filter(test => test.test_pass).length ?? 0

  return (
    <>
      <path
        id={id}
        className="react-flow__edge-path"
        d={edgePath}
        style={{
          stroke:
            errorCount > 0
              ? lighten(theme.palette.error.light, 0.3)
              : undefined,
        }}
      />
      <EdgeLabelRenderer>
        <Box
          onClick={toggleExpand}
          sx={{
            pointerEvents: "all",
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            zIndex: 20,
            width: expand ? 225 : undefined,
            overflowWrap: "break-word",
            p: 0,
            cursor: "pointer",
          }}
          className="nodrag nopan"
          data-testid="test-edge"
        >
          {expand ? (
            <Card variant="outlined">
              <CardContent sx={{ py: 1, "&:last-child": { pb: 1 } }}>
                <TestSection
                  tests={data?.tests?.filter(t => !t.test_pass)}
                  type="Failures"
                  icon={
                    <CancelOutlined
                      sx={{ color: theme => theme.palette.error.main }}
                    />
                  }
                />
                <TestSection
                  tests={data?.tests?.filter(t => t.test_pass)}
                  type="Passes"
                  icon={
                    <CheckCircleOutline
                      sx={{ color: theme => theme.palette.success.main }}
                    />
                  }
                  sx={{ mt: 2 }}
                />
              </CardContent>
            </Card>
          ) : (
            <TestsSummary
              errorCount={errorCount}
              passCount={passCount}
              data-testid="test-edge"
            />
          )}
        </Box>
      </EdgeLabelRenderer>
    </>
  )
}

export default TestEdge
