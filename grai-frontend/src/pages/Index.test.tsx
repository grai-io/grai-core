import React from "react"
import { renderWithRouter } from "testing"
import Index from "./Index"

test("renders", async () => {
  renderWithRouter(<Index />)
})
