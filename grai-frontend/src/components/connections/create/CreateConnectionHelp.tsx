import { Link } from "@mui/material"
import HelpItem from "components/help/HelpItem"
import HelpSection from "components/help/HelpSection"
import React from "react"
import { Link as RouterLink, useParams } from "react-router-dom"

interface Connector {
  name: string
}

type CreateConnectionHelpProps = {
  connector: Connector | null
}

const CreateConnectionHelp: React.FC<CreateConnectionHelpProps> = ({
  connector,
}) => {
  const { workspaceId } = useParams()

  return (
    <HelpSection>
      <HelpItem title="Read our docs">
        Not sure where to start? Check out the{" "}
        <Link href="https://docs.grai.io">docs for {connector?.name}</Link> for
        step-by-step instructions.
      </HelpItem>
      <HelpItem title="Invite a teammate">
        If you're missing credentials or connection info,{" "}
        <RouterLink to={`/workspaces/${workspaceId}/settings/memberships`}>
          invite a teammate
        </RouterLink>{" "}
        to join you in this Grai workspace.
      </HelpItem>
      <HelpItem title="Contact support">
        We're here to help! Chat with us if you feel stuck or have any
        questions.
      </HelpItem>
    </HelpSection>
  )
}

export default CreateConnectionHelp
