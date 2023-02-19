import { Outlet, Navigate, useLocation } from "react-router-dom"
import useAuth from "./useAuth"

type GuestRouteProps = {
  redirect?: string
}

const GuestRoute: React.FC<GuestRouteProps> = ({ redirect }) => {
  const { loggedIn } = useAuth()
  let location = useLocation()

  if (loggedIn)
    return <Navigate to={location.state?.redirect ?? redirect ?? "/"} replace />

  return <Outlet />
}

export default GuestRoute
