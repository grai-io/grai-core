import { Outlet, Navigate, useLocation } from "react-router-dom"
import useAuth from "./useAuth"

const PrivateRoute: React.FC = () => {
  const { loggedIn } = useAuth()
  let location = useLocation()

  if (!loggedIn) return <Navigate to="/login" state={{ redirect: location }} />

  return <Outlet />
}

export default PrivateRoute
