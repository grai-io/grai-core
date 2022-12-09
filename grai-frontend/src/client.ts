import { ApolloClient, InMemoryCache } from "@apollo/client"

const client = (token: string) =>
  new ApolloClient({
    uri: "http://localhost:8000/graphql/", //process.env.REACT_APP_API_URL,
    // credentials: "include",
    cache: new InMemoryCache(),
    connectToDevTools: true,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

export default client
