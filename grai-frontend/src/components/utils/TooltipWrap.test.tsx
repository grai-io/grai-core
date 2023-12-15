import { render, screen } from "testing"
import TooltipWrap from "./TooltipWrap"

test("renders", async () => {
  render(
    <TooltipWrap title="title" show>
      <>Hello</>
    </TooltipWrap>,
    {
      withRouter: true,
    },
  )

  await screen.findByText("Hello")
})

test("renders no show", async () => {
  render(
    <TooltipWrap title={null} show={false}>
      <>Hello</>
    </TooltipWrap>,
    {
      withRouter: true,
    },
  )

  await screen.findByText("Hello")
})
