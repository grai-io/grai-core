import {
  ApolloClient,
  createHttpLink,
  from,
  InMemoryCache,
} from "@apollo/client"
import { onError } from "@apollo/client/link/error"

const client = (logoutUser: () => void) => {
  const baseURL =
    window._env_?.REACT_APP_SERVER_URL ??
    process.env.REACT_APP_SERVER_URL ??
    "http://localhost:8000"

  const httpLink = createHttpLink({
    uri: `${baseURL}/graphql/`,
    credentials: "include",
    // headers: {
    //   Authorization: `Bearer ${tokens?.access}`,
    // },
  })

  const errorLink = onError(({ graphQLErrors }) => {
    if (graphQLErrors?.[0].message === "User is not authenticated123") {
      logoutUser()
    }
  })

  return new ApolloClient({
    cache: new InMemoryCache(),
    link: from([errorLink, httpLink]),
    connectToDevTools: true,
  })
}

export default client
