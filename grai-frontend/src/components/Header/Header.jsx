import React from 'react'
import PropTypes from "prop-types"
import { Box, useColorModeValue,} from '@chakra-ui/react'
import { NavContent } from './NavContent'


export const Header = ({ siteTitle }) => {
  const backgroundColor = useColorModeValue('white', 'web')
  return (
    <Box
      as="header"
      background={backgroundColor}
      // h={["80px", null, "44px", "60px", "80px"]}
    >
      <Box 
        className="nav-box" 
        // height="100%"
      >
        <NavContent.Mobile
          display={{
            base: "flex",
            md: "flex",
            lg: "none",
          }}
        />
        <NavContent.Desktop
          display={{
            base: "none",
            md: "none",
            lg: "flex",
          }}
        />
      </Box>

    </Box>
    )
}

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

