import React from "react"
import { Position, ReactFlowProvider } from "reactflow"
import { render } from "testing"
import ErrorEdge from "./ErrorEdge"

test("renders", async () => {
  render(
    <ReactFlowProvider>
      <svg>
        <ErrorEdge
          id="1"
          sourceX={100}
          sourceY={100}
          targetX={200}
          targetY={200}
          sourcePosition={Position.Top}
          targetPosition={Position.Bottom}
          source="1"
          target="2"
          data={{}}
        />
      </svg>
    </ReactFlowProvider>
  )
})

test("renders errors", async () => {
  const data = {
    errors: [
      {
        message: "Error Message",
      },
    ],
  }

  render(
    <ReactFlowProvider>
      <svg>
        <ErrorEdge
          id="1"
          sourceX={100}
          sourceY={100}
          targetX={200}
          targetY={200}
          sourcePosition={Position.Top}
          targetPosition={Position.Bottom}
          source="1"
          target="2"
          data={data}
        />
      </svg>
    </ReactFlowProvider>
  )

  // await waitFor(() => {
  //   expect(screen.getByText("Error Message")).toBeInTheDocument()
  // })
})
