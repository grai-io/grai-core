import React from "react"
import { Link } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link as RouterLink } from "react-router-dom"
import HelpItem from "components/help/HelpItem"
import HelpSection from "components/help/HelpSection"

interface Connector {
  name: string
  metadata?: {
    docs_url?: string | null
  } | null
}

type CreateConnectionHelpProps = {
  connector: Connector | null
}

const CreateConnectionHelp: React.FC<CreateConnectionHelpProps> = ({
  connector,
}) => {
  const { routePrefix } = useWorkspace()

  return (
    <HelpSection>
      <HelpItem title="Read our docs">
        Not sure where to start? Check out the{" "}
        <Link
          href={connector?.metadata?.docs_url ?? "https://docs.grai.io"}
          target="_blank"
        >
          docs for {connector?.name}
        </Link>{" "}
        for step-by-step instructions.
      </HelpItem>
      <HelpItem title="Invite a teammate">
        If you're missing credentials or connection info,{" "}
        <RouterLink to={`${routePrefix}/settings/memberships`}>
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
