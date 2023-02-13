/* istanbul ignore file */
import { ApolloClient, from, InMemoryCache } from "@apollo/client"
import { onError } from "@apollo/client/link/error"
import { createUploadLink } from "apollo-upload-client"

declare global {
  interface Window {
    _env_: any
  }
}

const make_client = (logoutUser: () => void) => {
  const baseURL =
    window._env_?.REACT_APP_SERVER_URL ??
    process.env.REACT_APP_SERVER_URL ??
    "http://localhost:8000"

  const uploadLink = createUploadLink({
    uri: `${baseURL}/graphql/`,
    credentials: "include",
  })

  const errorLink = onError(({ graphQLErrors }) => {
    if (graphQLErrors?.[0].message === "User is not authenticated") {
      logoutUser()
    }
  })

  return new ApolloClient({
    cache: new InMemoryCache(),
    link: from([errorLink, uploadLink]),
    connectToDevTools: true,
  })
}

export default make_client
