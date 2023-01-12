import { Outlet, Navigate, useLocation } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "./AuthContext"

type GuestRouteProps = {
  redirect?: string
}

const GuestRoute: React.FC<GuestRouteProps> = ({ redirect }) => {
  const { loggedIn } = useContext(AuthContext)
  let location = useLocation()

  if (loggedIn)
    return <Navigate to={location.state.redirect ?? redirect ?? "/"} replace />

  return <Outlet />
}

export default GuestRoute
