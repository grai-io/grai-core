import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import VerifyEmail, { VERIFY_EMAIL } from "./VerifyEmail"

test("renders", async () => {
  render(<VerifyEmail />, {
    route: "/email-verification?token=abc&uid=1234",
    path: "email-verification",
    routes: ["/"],
  })

  expect(screen.getByRole("progressbar")).toBeTruthy()

  await screen.findByText("New Page")
})

test("missing token", async () => {
  render(<VerifyEmail />, {
    route: "/email-verification?uid=1234",
    path: "email-verification",
    routes: ["/"],
  })

  await screen.findByText("Missing required token")
})

test("missing uid", async () => {
  render(<VerifyEmail />, {
    route: "/email-verification?token=abc",
    path: "email-verification",
    routes: ["/"],
  })

  await screen.findByText("Missing required token")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: VERIFY_EMAIL,
        variables: {
          uid: "1234",
          token: "abc",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<VerifyEmail />, {
    route: "/email-verification?token=abc&uid=1234",
    path: "email-verification",
    routes: ["/"],
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
