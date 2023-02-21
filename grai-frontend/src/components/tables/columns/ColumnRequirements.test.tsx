import React from "react"
import { render } from "testing"
import ColumnRequirements from "./ColumnRequirements"

test("renders", async () => {
  const edges = [
    {
      type: "unique",
      text: "Unique",
      source: { name: "s1", display_name: "s1" },
      passed: true,
      preserved: true,
    },
  ]

  render(<ColumnRequirements edges={edges} />)
})

test("renders empty", async () => {
  render(<ColumnRequirements edges={[]} />)
})

test("renders failed", async () => {
  const edges = [
    {
      type: "unique",
      text: "Unique",
      source: { name: "s1", display_name: "s1" },
      passed: false,
      preserved: true,
    },
  ]

  render(<ColumnRequirements edges={edges} />)
})

test("renders not preserved", async () => {
  const edges = [
    {
      type: "unique",
      text: "Unique",
      source: { name: "s1", display_name: "s1" },
      passed: false,
      preserved: false,
    },
  ]

  render(<ColumnRequirements edges={edges} />)
})
