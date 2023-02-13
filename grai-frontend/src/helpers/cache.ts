import { ApolloCache } from "@apollo/client"

export const clearWorkspace = (cache: ApolloCache<any>, id: string) => {
  cache.evict({
    id: cache.identify({
      id,
      __typename: "Workspace",
    }),
    fieldName: "nodes",
  })
  cache.evict({
    id: cache.identify({
      id,
      __typename: "Workspace",
    }),
    fieldName: "tables",
  })
  cache.evict({
    id: cache.identify({
      id,
      __typename: "Workspace",
    }),
    fieldName: "edges",
  })
  cache.evict({
    id: cache.identify({
      id,
      __typename: "Workspace",
    }),
    fieldName: "other_edges",
  })
}
