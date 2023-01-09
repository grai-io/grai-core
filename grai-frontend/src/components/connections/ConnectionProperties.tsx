import { Edit } from "@mui/icons-material"
import { Box, Button, Stack, Typography } from "@mui/material"
import NodeDetailRow from "components/nodes/NodeDetailRow"
import React, { useState } from "react"
import EditConnectionDialog from "./EditConnectionDialog"

export interface ConnectorMetadataField {
  name: string
  label?: string
  secret?: boolean
  required?: boolean
  default?: string | number
}

export interface ConnectorMetadata {
  fields?: ConnectorMetadataField[]
}

interface Connector {
  id: string
  name: string
  metadata: ConnectorMetadata
}

interface Connection {
  id: string
  namespace: string
  name: string
  connector: Connector
  metadata: any
}

type ConnectionPropertiesProps = {
  connection: Connection
}

const ConnectionProperties: React.FC<ConnectionPropertiesProps> = ({
  connection,
}) => {
  const [open, setOpen] = useState(false)

  const fields = connection.connector.metadata?.fields

  const handleClick = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <>
      <NodeDetailRow label="Connection Properties">
        <Box sx={{ display: "flex" }}>
          <Stack spacing={1} sx={{ flexGrow: 1 }}>
            {fields
              ?.filter(f => !f.secret)
              .map(field => (
                <Typography key={field.name} variant="body2">
                  {field.label ?? field.name}:{" "}
                  {connection.metadata && connection.metadata[field.name]}
                </Typography>
              ))}
            {fields
              ?.filter(f => f.secret)
              .map(field => (
                <Typography key={field.name} variant="body2">
                  {field.label ?? field.name}: ******
                </Typography>
              ))}
          </Stack>
          <Box>
            <Button
              variant="outlined"
              startIcon={<Edit />}
              size="small"
              onClick={handleClick}
            >
              Edit
            </Button>
          </Box>
        </Box>
      </NodeDetailRow>
      <EditConnectionDialog
        open={open}
        onClose={handleClose}
        connection={connection}
      />
    </>
  )
}

export default ConnectionProperties
