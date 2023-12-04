import React from "react"
import { Box, Link } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import HelpItem from "components/help/HelpItem"
import Docs from "components/icons/Docs"
import InviteUser from "components/icons/InviteUser"

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
    <Box>
      <HelpItem title="Invite a teammate" icon={<InviteUser />} color="#FAF5FF">
        If you're missing credentials or connection info,{" "}
        <RouterLink to={`${routePrefix}/settings/memberships`}>
          invite a teammate
        </RouterLink>{" "}
        to join you in this Grai workspace.
      </HelpItem>
      <HelpItem title="Docs" icon={<Docs />} color="#F0F6FF">
        Not sure where to start? Check out the{" "}
        <Link
          href={connector?.metadata?.docs_url ?? "https://docs.grai.io"}
          target="_blank"
        >
          docs for {connector?.name}
        </Link>{" "}
        for step-by-step instructions.
      </HelpItem>
    </Box>
  )
}

export default CreateConnectionHelp
