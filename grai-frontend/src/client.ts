/* istanbul ignore file */
import { ApolloClient, from, InMemoryCache, TypePolicies } from "@apollo/client"
import { onError } from "@apollo/client/link/error"
import DebounceLink from "apollo-link-debounce"
import { createUploadLink } from "apollo-upload-client"

declare global {
  interface Window {
    _env_: any
  }
}

const DEFAULT_DEBOUNCE_TIMEOUT = 100

export const typePolicies: TypePolicies = {
  Query: {
    fields: {
      workspace: {
        merge: true,
      },
    },
  },
  Workspace: {
    fields: {
      runs: {
        merge: true,
      },
    },
  },
}

export const cache = new InMemoryCache({
  typePolicies,
})

export const baseURL =
  window._env_?.REACT_APP_SERVER_URL ??
  process.env.REACT_APP_SERVER_URL ??
  "http://localhost:8000"

const make_client = (logoutUser: () => void) => {
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
    cache,
    link: from([
      new DebounceLink(DEFAULT_DEBOUNCE_TIMEOUT),
      errorLink,
      uploadLink,
    ]),
    connectToDevTools: true,
  })
}

export default make_client
