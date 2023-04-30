import { render, screen } from "testing"
import ReportCard from "./ReportCard"

test("renders", async () => {
  const report = {
    id: "1",
    connection: {
      name: "Connection 1",
      connector: {
        name: "Connector 1",
        icon: null,
      },
      temp: false,
    },
    commit: null,
  }

  render(<ReportCard report={report} />, {
    withRouter: true,
  })

  expect(screen.getByText(/Connection 1/i)).toBeInTheDocument()
  expect(screen.queryByText(/Connector 1/i)).not.toBeInTheDocument()
})

test("renders icon", async () => {
  const report = {
    id: "1",
    connection: {
      name: "Connection 1",
      connector: {
        name: "Connector 1",
        icon: "icon",
      },
      temp: false,
    },
    commit: null,
  }

  render(<ReportCard report={report} />, {
    withRouter: true,
  })

  expect(screen.getByText(/Connection 1/i)).toBeInTheDocument()
  expect(screen.queryByText(/Connector 1/i)).not.toBeInTheDocument()
})

test("renders temp", async () => {
  const report = {
    id: "1",
    connection: {
      name: "Connection 1",
      connector: {
        name: "Connector 1",
        icon: null,
      },
      temp: true,
    },
    commit: null,
  }

  render(<ReportCard report={report} />, {
    withRouter: true,
  })

  expect(screen.queryByText(/Connection 1/i)).not.toBeInTheDocument()
  expect(screen.getByText(/Connector 1/i)).toBeInTheDocument()
})

test("renders commit", async () => {
  const report = {
    id: "1",
    connection: {
      name: "Connection 1",
      connector: {
        name: "Connector 1",
        icon: null,
      },
      temp: false,
    },
    commit: {
      repository: {
        owner: "owner",
        repo: "repo",
      },
    },
  }

  render(<ReportCard report={report} />, {
    withRouter: true,
  })

  expect(screen.getByText(/Connection 1/i)).toBeInTheDocument()
  expect(screen.queryByText(/Connector 1/i)).not.toBeInTheDocument()

  expect(screen.getByText(/owner\/repo/i)).toBeInTheDocument()
})
