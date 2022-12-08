import { ApolloClient, InMemoryCache } from "@apollo/client"

const client = new ApolloClient({
  uri: "http://localhost:8000/graphql/", //process.env.REACT_APP_API_URL,
  // credentials: "include",
  cache: new InMemoryCache(),
  connectToDevTools: true,
})

export default client
