import React from "react"
import { Link } from "@mui/material"
import HelpItem from "components/help/HelpItem"
import HelpSection from "components/help/HelpSection"

const ScheduleHelp: React.FC = () => (
  <HelpSection>
    <HelpItem title="Read our docs">
      Not sure where to start? Check out the{" "}
      <Link href="https://docs.grai.io">docs for schedules</Link> for
      step-by-step instructions.
    </HelpItem>
    <HelpItem title="Contact support">
      We're here to help! Chat with us if you feel stuck or have any questions.
    </HelpItem>
  </HelpSection>
)

export default ScheduleHelp
