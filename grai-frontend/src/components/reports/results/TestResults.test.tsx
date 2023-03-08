import React from "react"
import { render, screen } from "testing"
import TestResults from "./TestResults"

test("renders", async () => {
  const errors = [
    {
      source: "s1",
      destination: "d1",
      test: "t1",
      message: "test message",
      test_pass: false,
    },
  ]

  render(<TestResults errors={errors} />)

  expect(screen.getByText("test message")).toBeInTheDocument()
})

test("renders empty", async () => {
  render(<TestResults errors={[]} />)
})
