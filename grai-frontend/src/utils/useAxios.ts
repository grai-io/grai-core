import axios from "axios"
import jwt_decode from "jwt-decode"
import dayjs from "dayjs"
import { useContext } from "react"
import AuthContext, { Tokens } from "../components/auth/AuthContext"

const baseURL = "http://localhost:8000/api/v1"

const useAxios = () => {
  const { authTokens, setUser, setAuthTokens } = useContext(AuthContext)

  const axiosInstance = axios.create({
    baseURL,
    headers: {
      Authorization: `Bearer ${authTokens?.access}`,
    },
  })

  axiosInstance.interceptors.request.use(
    async req => {
      const user = jwt_decode(authTokens?.access ?? "") as any
      const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1

      if (!isExpired) return req

      if (!authTokens?.refresh) {
        setAuthTokens(null)
        setUser(null)

        return req
      }

      const response = await axios
        .post(`${baseURL}/auth/jwttoken/refresh/`, {
          refresh: authTokens?.refresh,
        })
        .catch(error => {
          if (error.response.status === 401) {
            setAuthTokens(null)
            setUser(null)

            return
          }

          throw error
        })

      if (!response) return req

      const updatedAuthTokens: Tokens = authTokens
        ? { refresh: authTokens.refresh, access: response.data.access }
        : { access: response.data.access, refresh: "" }

      localStorage.setItem("authTokens", JSON.stringify(updatedAuthTokens))

      setAuthTokens(updatedAuthTokens)
      setUser(jwt_decode(response.data.access))

      if (req.headers)
        req.headers.Authorization = `Bearer ${response.data.access}`

      return req
    },
    error => {
      if (error.response.status === 401) {
        setAuthTokens(null)
        setUser(null)

        return
      }

      throw error
    }
  )

  return axiosInstance
}

export default useAxios
