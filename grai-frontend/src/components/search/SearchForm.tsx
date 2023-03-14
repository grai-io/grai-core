import React from "react"
import { Divider, Box, List, Typography } from "@mui/material"
import {
  useHits,
  useSearchBox,
  useInstantSearch,
} from "react-instantsearch-hooks-web"
import SearchHitRow, { SearchHit } from "./SearchHitRow"
import SearchTextbox from "./SearchTextbox"

type SearchFormProps = {
  onClose: () => void
  onError: (error: Error) => void
}

const SearchForm: React.FC<SearchFormProps> = ({ onClose, onError }) => {
  const { query } = useSearchBox()
  const { hits } = useHits<SearchHit>()
  const { error } = useInstantSearch()

  if (error) onError(error)

  return (
    <>
      <SearchTextbox onClose={onClose} />
      {query.length > 0 && (
        <>
          <Divider />
          <Box sx={{ height: 700, overflowY: "scroll" }}>
            <List>
              {hits.map(hit => (
                <SearchHitRow key={hit.id} hit={hit} />
              ))}
            </List>
            {hits.length === 0 && (
              <Box sx={{ textAlign: "center", p: 10 }}>
                <Typography variant="h6">No search results</Typography>
              </Box>
            )}
          </Box>
        </>
      )}
    </>
  )
}

export default SearchForm
