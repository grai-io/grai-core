import React from "react"
import userEvent from "@testing-library/user-event"
import { fireEvent, render, renderWithRouter, screen, waitFor } from "testing"
import BaseNode from "./BaseNode"
import { ReactFlowProvider } from "reactflow"

const data = {
  id: "1234",
  label: "Node Label",
  highlight: false,
  columns: [
    {
      displayName: "c1",
      name: "c1",
    },
  ],
  hiddenSourceTables: ["a"],
  hiddenDestinationTables: ["b"],
  expanded: false,
  onExpand: (value: boolean) => {},
  onShow: (values: string[]) => {},
}

test("renders", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeTruthy()
  })
})

test("renders no columns", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={{ ...data, columns: [] }} />
    </ReactFlowProvider>
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeTruthy()
  })
})

test("renders multiple columns", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          columns: [
            ...data.columns,
            {
              name: "c2",
            },
          ],
          expanded: true,
        }}
      />
    </ReactFlowProvider>
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("c1")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("c2")).toBeTruthy()
  })
})

test("highlight", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          highlight: true,
        }}
      />
    </ReactFlowProvider>
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeTruthy()
  })
})

test("expanded", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          expanded: true,
        }}
      />
    </ReactFlowProvider>
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("c1")).toBeTruthy()
  })
})

test("expand", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>
  )

  await user.click(screen.getByTestId("ArrowDropDownIcon"))
})

test("context menu", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await user.keyboard("{escape}")
})

test("context menu show lineage", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await user.click(screen.getAllByRole("menuitem")[0])
})

test("context menu show upstream dependents", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await user.click(
    screen.getByRole("menuitem", { name: /Show upstream dependents/i })
  )
})

test("context menu show downstream dependents", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await user.click(
    screen.getByRole("menuitem", { name: /Show downstream dependents/i })
  )
})

test("context menu show downstream dependents", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    { routes: ["/workspaces/:workspaceId/nodes/:nodeId"] }
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await user.click(
    screen.getByRole("menuitem", { name: /Show profile for this table/i })
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})
