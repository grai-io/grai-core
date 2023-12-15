import { render, screen } from "testing"
import Settings from "./Settings"

test("redirects", async () => {
  render(<Settings />, {
    path: "/:organisationName/:workspaceName/settings",
    route: "/default/demo/settings",
    routes: ["/default/demo/settings/profile"],
  })

  await screen.findByText("New Page")
})
