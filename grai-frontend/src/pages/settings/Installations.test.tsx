import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import { GET_REPOSITORIES } from "components/settings/installations/GitHubInstallation"
import Installations from "./Installations"

test("renders", async () => {
  render(<Installations />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: "Settings" })

  await screen.findByRole("heading", { name: /Installations/i })

  await screen.findAllByTestId("GitHubIcon")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Installations />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<Installations />, { mocks, withRouter: true })

  await screen.findByText("Sorry something has gone wrong")
})

test("renders no installations", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            repositories: {
              data: [],
            },
          },
        },
      },
    },
  ]

  render(<Installations />, { mocks, withRouter: true })

  await screen.findByText("Connect GitHub")
})
