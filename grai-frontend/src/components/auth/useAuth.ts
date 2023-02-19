import { useContext } from "react"
import AuthContext from "./AuthContext"

const useAuth = () => useContext(AuthContext)

export default useAuth
