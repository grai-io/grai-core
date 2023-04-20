import React from "react"
import { Card, CardContent, Link, Typography } from "@mui/material"
import RegisterForm from "./RegisterForm"

const RegisterCard: React.FC = () => (
  <Card
    sx={{
      boxShadow: "0 10px 20px 0 rgb(0 0 0 / 0.04)",
      borderRadius: "20px",
      borderColor: "rgba(0, 0, 0, 0.06)",
      borderWidth: 1,
      borderStyle: "solid",
    }}
  >
    <CardContent sx={{ p: 5 }}>
      <Typography variant="h6" sx={{ mb: 1, fontWeight: "bold", fontSize: 24 }}>
        Register for an account
      </Typography>
      <RegisterForm />
      <Typography
        variant="body2"
        sx={{ color: theme => theme.palette.grey[600], lineHeight: 1.5 }}
      >
        By creating an account, you agree to our{" "}
        <Link
          href="https://www.grai.io/terms"
          sx={{
            textDecoration: "none",
            color: theme => theme.palette.grey[900],
            "&:hover": {
              textDecoration: "underline",
            },
          }}
          target="_blank"
        >
          Terms of Service
        </Link>{" "}
        and{" "}
        <Link
          href="https://www.grai.io/privacy"
          sx={{
            textDecoration: "none",
            color: theme => theme.palette.grey[900],
            "&:hover": {
              textDecoration: "underline",
            },
          }}
          target="_blank"
        >
          Privacy Policy
        </Link>
        .
      </Typography>
    </CardContent>
  </Card>
)

export default RegisterCard
