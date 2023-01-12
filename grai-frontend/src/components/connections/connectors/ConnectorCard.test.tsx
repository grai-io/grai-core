import React from "react"
import { render } from "testing"
import ConnectorCard from "./ConnectorCard"

test("renders", async () => {
  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
      }}
      onSelect={() => {}}
    />
  )
})

test("coming soon", async () => {
  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
        coming_soon: true,
      }}
      onSelect={() => {}}
    />
  )
})
