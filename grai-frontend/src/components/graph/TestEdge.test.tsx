import React from "react"
import userEvent from "@testing-library/user-event"
import ReactFlow, {
  Edge,
  EdgeTypes,
  Position,
  ReactFlowProvider,
} from "reactflow"
import { act, render, screen, waitFor } from "testing"
import TestEdge, { TestData } from "./TestEdge"

test("renders", async () => {
  render(
    <ReactFlowProvider>
      <svg>
        <TestEdge
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
    tests: [
      {
        message: "Error Message",
      },
      {
        message: "Pass Message",
        test_pass: true,
      },
    ],
  }

  render(
    <ReactFlowProvider>
      <svg>
        <TestEdge
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
})

test("expand", async () => {
  const user = userEvent.setup()

  const nodes = [
    { id: "1", position: { x: 0, y: 0 }, data: { label: "1" } },
    { id: "2", position: { x: 0, y: 100 }, data: { label: "2" } },
  ]

  const edges: Edge<TestData>[] = [
    {
      id: "e1-2",
      source: "1",
      target: "2",
      type: "test",
      data: {
        tests: [
          {
            message: "Error Message",
            test_pass: false,
          },
          {
            message: "Pass Message",
            test_pass: true,
          },
        ],
      },
    },
  ]

  const edgeTypes: EdgeTypes = {
    test: TestEdge,
  }

  render(<ReactFlow nodes={nodes} edges={edges} edgeTypes={edgeTypes} />)

  await waitFor(() => {
    expect(screen.getByTestId("test-edge")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("test-edge")))
})

test("renders only success", async () => {
  const user = userEvent.setup()

  const nodes = [
    { id: "1", position: { x: 0, y: 0 }, data: { label: "1" } },
    { id: "2", position: { x: 0, y: 100 }, data: { label: "2" } },
  ]

  const edges: Edge<TestData>[] = [
    {
      id: "e1-2",
      source: "1",
      target: "2",
      type: "test",
      data: {
        tests: [
          {
            message: "Pass Message",
            test_pass: true,
          },
          {
            message: "Pass Message2",
            test_pass: true,
          },
        ],
      },
    },
  ]

  const edgeTypes: EdgeTypes = {
    test: TestEdge,
  }

  render(<ReactFlow nodes={nodes} edges={edges} edgeTypes={edgeTypes} />)

  await waitFor(() => {
    expect(screen.getByTestId("test-edge")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("test-edge")))
})
