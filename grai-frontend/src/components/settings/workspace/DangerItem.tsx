import React from "react"
import { LoadingButton } from "@mui/lab"
import { Card, List, ListItem, ListItemText } from "@mui/material"

type DangerItemProps = {
  onClick: () => void
  primary: string
  secondary?: string
  buttonText: string
  loading?: boolean
}

const DangerItem: React.FC<DangerItemProps> = ({
  onClick,
  primary,
  secondary,
  buttonText,
  loading,
}) => (
  <Card
    variant="outlined"
    sx={{ borderColor: theme => theme.palette.error.dark, mb: 2 }}
  >
    <List>
      <ListItem
        secondaryAction={
          <LoadingButton
            variant="outlined"
            color="error"
            onClick={onClick}
            loading={loading}
          >
            {buttonText}
          </LoadingButton>
        }
      >
        <ListItemText primary={primary} secondary={secondary} />
      </ListItem>
    </List>
  </Card>
)

export default DangerItem
