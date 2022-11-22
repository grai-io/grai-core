import { Outlet, Navigate } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "./AuthContext"

const GuestRoute = () => {
  const { user } = useContext(AuthContext)

  if (user) return <Navigate to="/" />

  return <Outlet />
}

export default GuestRoute
