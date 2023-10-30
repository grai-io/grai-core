import React from "react"
import {
  AccountCircle,
  DataUsage,
  HelpOutline,
  Menu,
} from "@mui/icons-material"
import {
  Box,
  Button,
  Dialog,
  Link,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material"
import DialogTitle from "components/dialogs/DialogTitle"

type SampleDataDialogProps = {
  open: boolean
  onClose: () => void
}

const SampleDataDialog: React.FC<SampleDataDialogProps> = ({
  open,
  onClose,
}) => (
  <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
    <DialogTitle onClose={onClose}>Welcome to your new workspace</DialogTitle>
    <List sx={{ px: 2 }}>
      <ListItem>
        <ListItemIcon>
          <DataUsage />
        </ListItemIcon>
        <ListItemText>
          <Typography variant="body1">
            We have populated this workspace with some sample data, to help you
            explore everything Grai has to offer.
          </Typography>
        </ListItemText>
      </ListItem>

      <ListItem>
        <ListItemIcon>
          <Menu />
        </ListItemIcon>
        <ListItemText>
          <Typography variant="body1">
            Why not have a look at the different pages from the sidebar.
          </Typography>
        </ListItemText>
      </ListItem>

      <ListItem>
        <ListItemIcon>
          <AccountCircle />
        </ListItemIcon>
        <ListItemText>
          <Typography variant="body1">
            To get started on your own workspace, choose Change Workspace from
            the profile menu, bottom left.
          </Typography>
        </ListItemText>
      </ListItem>

      <ListItem>
        <ListItemIcon>
          <HelpOutline />
        </ListItemIcon>
        <ListItemText>
          <Typography variant="body1">
            If you need help, why not look in the{" "}
            <Link href="https://docs.grai.io" target="_blank">
              docs
            </Link>
            , or contact us through the chat icon in the bottom right.
          </Typography>
        </ListItemText>
      </ListItem>
    </List>

    <Box sx={{ textAlign: "center", pb: 3, pt: 1 }}>
      <Button variant="contained" size="large" onClick={onClose}>
        Get started
      </Button>
    </Box>
  </Dialog>
)

export default SampleDataDialog
