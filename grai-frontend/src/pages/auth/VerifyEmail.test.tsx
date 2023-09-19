import React from "react"
import { render, screen, waitFor } from "testing"
import VerifyEmail, { VERIFY_EMAIL } from "./VerifyEmail"
import { GraphQLError } from "graphql"

test("renders", async () => {
  render(<VerifyEmail />, {
    route: "/email-verification?token=abc&uid=1234",
    path: "email-verification",
    routes: ["/"],
  })

  expect(screen.getByRole("progressbar")).toBeTruthy()

  await waitFor(async () =>
    expect(screen.getByText("New Page")).toBeInTheDocument(),
  )
})

test("missing token", async () => {
  render(<VerifyEmail />, {
    route: "/email-verification?uid=1234",
    path: "email-verification",
    routes: ["/"],
  })

  await waitFor(async () =>
    expect(screen.getByText("Missing required token")).toBeInTheDocument(),
  )
})

test("missing uid", async () => {
  render(<VerifyEmail />, {
    route: "/email-verification?token=abc",
    path: "email-verification",
    routes: ["/"],
  })

  await waitFor(async () =>
    expect(screen.getByText("Missing required token")).toBeInTheDocument(),
  )
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
