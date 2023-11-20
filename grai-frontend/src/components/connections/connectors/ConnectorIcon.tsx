import React, { ReactNode } from "react"

export interface Connector {
  icon: string | ReactNode
  name: string
}

type ConnectorIconProps = {
  connector: Connector
}

const ConnectorIcon: React.FC<ConnectorIconProps> = ({ connector }) => {
  if (typeof connector.icon === "string")
    return (
      <img
        src={connector.icon}
        alt={`${connector.name} logo`}
        style={{ height: 28, width: 28 }}
      />
    )

  return <>{connector.icon}</>
}

export default ConnectorIcon
