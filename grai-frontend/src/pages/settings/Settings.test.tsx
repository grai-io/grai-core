import React from "react"
import { render, screen, waitFor } from "testing"
import Settings from "./Settings"

test("redirects", async () => {
  render(<Settings />, {
    path: "/:organisationName/:workspaceName/settings",
    route: "/default/demo/settings",
    routes: ["/default/demo/settings/profile"],
  })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})
