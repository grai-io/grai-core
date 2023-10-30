import React, { ReactNode } from "react"
import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client"
import { SchemaLink } from "@apollo/client/link/schema"
import { MockedProvider, MockedResponse } from "@apollo/client/testing"
import { addMocksToSchema, IMocks } from "@graphql-tools/mock"
import { makeExecutableSchema } from "@graphql-tools/schema"
import { typePolicies } from "client"
import { buildClientSchema, printSchema } from "graphql/utilities"
import introspectionResult from "./schema.json"

type AutoMockedProviderProps = {
  children: ReactNode
  mockResolvers?: IMocks
  mocks?: readonly MockedResponse<Record<string, any>>[]
  cache: InMemoryCache
}

const AutoMockedProvider: React.FC<AutoMockedProviderProps> = ({
  children,
  mockResolvers,
  mocks,
  cache,
}) => {
  if (mocks)
    return (
      <MockedProvider
        mocks={mocks}
        addTypename={false}
        cache={
          new InMemoryCache({
            addTypename: false,
            typePolicies,
          })
        }
      >
        {children}
      </MockedProvider>
    )

  // 1) Convert JSON schema into Schema Definition Language
  const schemaSDL = printSchema(
    buildClientSchema({ __schema: introspectionResult.__schema as any }),
  )

  // 2) Make schema "executable"
  const schema = makeExecutableSchema({
    typeDefs: schemaSDL,
    resolverValidationOptions: {
      // requireResolversForResolveType: false,
    },
  })

  // 3) Apply mock resolvers to executable schema
  const schemaWithMocks = addMocksToSchema({ schema, mocks: mockResolvers })

  // 4) Define ApolloClient (client variable used below)
  const client = new ApolloClient({
    link: new SchemaLink({ schema: schemaWithMocks }),
    cache,
  })

  return <ApolloProvider client={client}>{children}</ApolloProvider>
}

export default AutoMockedProvider
