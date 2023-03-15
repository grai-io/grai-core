import React, { useState } from "react"
import {
  ArrowDownward,
  ArrowUpward,
  SubdirectoryArrowLeft,
} from "@mui/icons-material"
import { Divider, Box, List, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
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
  const { workspaceNavigate } = useWorkspace()

  const { query } = useSearchBox()
  const { hits } = useHits<SearchHit>()
  const { error } = useInstantSearch()

  const [selected, setSelected] = useState<string>()

  if (error) onError(error)

  const handleKeyPress = (event: React.KeyboardEvent<HTMLDivElement>) => {
    switch (event.code) {
      case "ArrowDown":
        const indexDown = hits.findIndex(hit => hit.id === selected)
        const nextIndexDown = indexDown + 1
        if (nextIndexDown < hits.length) {
          setSelected(hits[nextIndexDown].id)
        }
        return
      case "ArrowUp":
        const indexUp = hits.findIndex(hit => hit.id === selected)
        const nextIndexUp = indexUp - 1
        if (nextIndexUp >= 0) {
          setSelected(hits[nextIndexUp].id)
        }
        return
      case "Enter":
        const hit = hits.find(hit => hit.id === selected)
        if (hit) {
          workspaceNavigate(
            hit.table_id ? `tables/${hit.table_id}` : `tables/${hit.id}`
          )
        }
    }
  }

  return (
    <Box onKeyDown={handleKeyPress}>
      <SearchTextbox onClose={onClose} />
      {query.length > 0 && (
        <>
          <Divider />
          <Box sx={{ height: 700, overflowY: "scroll" }}>
            <List>
              {hits.map(hit => (
                <SearchHitRow
                  key={hit.id}
                  hit={hit}
                  selected={selected === hit.id}
                />
              ))}
            </List>
            {hits.length === 0 && (
              <Box sx={{ textAlign: "center", p: 10 }}>
                <Typography variant="h6">No search results</Typography>
              </Box>
            )}
          </Box>
          <Divider />
          <Box sx={{ p: 2, display: "flex" }}>
            <Typography
              sx={{
                mr: 2,
                display: "flex",
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              <SubdirectoryArrowLeft sx={{ mr: 1 }} />
              to select
            </Typography>
            <Typography
              sx={{
                mr: 2,
                display: "flex",
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              <ArrowUpward />
              <ArrowDownward sx={{ mr: 1 }} /> to navigate
            </Typography>
            <Typography>esc to close</Typography>
          </Box>
        </>
      )}
    </Box>
  )
}

export default SearchForm
