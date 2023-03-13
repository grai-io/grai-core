import React from "react"
import { Divider, Box, List } from "@mui/material"
import { useHits, useSearchBox } from "react-instantsearch-hooks-web"
import SearchHitRow, { SearchHit } from "./SearchHitRow"
import SearchTextbox from "./SearchTextbox"

type SearchFormProps = {
  onClose: () => void
}

const SearchForm: React.FC<SearchFormProps> = ({ onClose }) => {
  const { query } = useSearchBox()
  const { hits } = useHits<SearchHit>()

  return (
    <>
      <SearchTextbox onClose={onClose} />
      {query.length > 0 && (
        <>
          <Divider />
          <Box sx={{ maxHeight: 700, overflowY: "scroll" }}>
            <List>
              {hits.map(hit => (
                <SearchHitRow key={hit.id} hit={hit} />
              ))}
            </List>
          </Box>
        </>
      )}
    </>
  )
}

export default SearchForm
