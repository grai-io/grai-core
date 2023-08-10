import React from "react"
import userEvent from "@testing-library/user-event"
import { ReactFlowProvider } from "reactflow"
import { act, fireEvent, render, screen, waitFor } from "testing"
import BaseNode, { BaseNodeData } from "./BaseNode"

const data: BaseNodeData = {
  id: "1234",
  label: "Node Label",
  data_source: "test",
  highlight: false,
  columns: [
    {
      id: "1",
      display_name: "c1",
    },
  ],
  hiddenSourceTables: ["a"],
  hiddenDestinationTables: ["b"],
  expanded: false,
  onExpand: (value: boolean) => {},
  onShow: (values: string[]) => {},
  searchHighlight: false,
  searchDim: false,
}

test("renders", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })
})

test("renders no columns", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode data={{ ...data, columns: [] }} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })
})

test("renders multiple columns", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          columns: [
            ...data.columns,
            {
              id: "2",
              display_name: "c2",
            },
          ],
          expanded: true,
        }}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("c1")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("c2")).toBeInTheDocument()
  })
})

test("highlight", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          highlight: true,
        }}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })
})

test("search highlight", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          searchHighlight: true,
        }}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })
})

test("search dim", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          searchDim: true,
        }}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })
})

test("expanded", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode
        data={{
          ...data,
          expanded: true,
        }}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Node Label")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("c1")).toBeInTheDocument()
  })
})

test("expand", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  await act(async () => await user.click(screen.getByTestId("ExpandMoreIcon")))
})

test("context menu", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await act(async () => await user.keyboard("{escape}"))
})

test("context menu show lineage", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await act(async () => await user.click(screen.getAllByRole("menuitem")[0]))
})

test("context menu show upstream dependents", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await act(
    async () =>
      await user.click(
        screen.getByRole("menuitem", { name: /Show upstream dependents/i }),
      ),
  )
})

test("context menu show downstream dependents", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await act(
    async () =>
      await user.click(
        screen.getByRole("menuitem", { name: /Show downstream dependents/i }),
      ),
  )
})

test("context menu show profile", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    { routes: ["/:organisationName/:workspaceName/nodes/:nodeId"] },
  )

  fireEvent.contextMenu(screen.getByText("Node Label"))

  await act(
    async () =>
      await user.click(
        screen.getByRole("menuitem", { name: /Show profile for this table/i }),
      ),
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("double click", async () => {
  render(
    <ReactFlowProvider>
      <BaseNode data={data} />
    </ReactFlowProvider>,
    { routes: ["/:organisationName/:workspaceName/nodes/:nodeId"] },
  )

  fireEvent.dblClick(screen.getByText("Node Label"))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})
