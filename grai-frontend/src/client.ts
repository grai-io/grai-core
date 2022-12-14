import {
  ApolloClient,
  createHttpLink,
  from,
  fromPromise,
  InMemoryCache,
} from "@apollo/client"
import { onError } from "@apollo/client/link/error"
import { Tokens } from "./components/auth/AuthContext"

const client = (
  tokens: Tokens | null,
  refresh: () => Promise<void>,
  logoutUser: () => void
) => {
  const httpLink = createHttpLink({
    uri: `${process.env.REACT_APP_SERVER_URL}/graphql/`,
    // credentials: "include",
    headers: {
      Authorization: `Bearer ${tokens?.access}`,
    },
  })

  const errorLink = onError(({ graphQLErrors, operation, forward }) => {
    if (
      graphQLErrors?.[0].message ===
      "{'detail': ErrorDetail(string='Given token not valid for any token type', code='token_not_valid'), 'code': ErrorDetail(string='token_not_valid', code='token_not_valid'), 'messages': [{'token_class': ErrorDetail(string='AccessToken', code='token_not_valid'), 'token_type': ErrorDetail(string='access', code='token_not_valid'), 'message': ErrorDetail(string='Token is invalid or expired', code='token_not_valid')}]}"
    ) {
      return fromPromise(refresh())
        .filter(value => Boolean(value))
        .flatMap(accessToken => {
          const oldHeaders = operation.getContext().headers
          // modify the operation context with a new token
          operation.setContext({
            headers: {
              ...oldHeaders,
              authorization: `Bearer ${accessToken}`,
            },
          })

          // retry the request, returning the new observable
          return forward(operation)
        })
    }
  })

  const logoutLink = onError(({ graphQLErrors }) => {
    console.log(graphQLErrors?.[0].message)

    if (
      graphQLErrors?.[0].message ===
      "{'detail': ErrorDetail(string='Given token not valid for any token type', code='token_not_valid'), 'code': ErrorDetail(string='token_not_valid', code='token_not_valid'), 'messages': [{'token_class': ErrorDetail(string='AccessToken', code='token_not_valid'), 'token_type': ErrorDetail(string='access', code='token_not_valid'), 'message': ErrorDetail(string='Token is invalid or expired', code='token_not_valid')}]}"
    ) {
      console.log("unathenticated")

      logoutUser()
    }
  })

  return new ApolloClient({
    cache: new InMemoryCache(),
    link: from([logoutLink, errorLink, httpLink]),
    connectToDevTools: true,
  })
}

export default client
