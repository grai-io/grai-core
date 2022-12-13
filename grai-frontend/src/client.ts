import { ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client"
import { onError } from "@apollo/client/link/error"

const client = (token: string, logoutUser: () => void) => {
  const httpLink = createHttpLink({
    uri: "http://localhost:8000/graphql/", //process.env.REACT_APP_API_URL,
    // credentials: "include",
    headers: {
      Authorization: `Bearer ${token}`,
    },
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
    link: logoutLink.concat(httpLink),
    connectToDevTools: true,
  })
}

export default client
