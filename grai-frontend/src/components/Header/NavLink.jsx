import {
  chakra,
  useColorModeValue as mode,
} from '@chakra-ui/react'
import * as React from 'react'

export const MobileNavLink = (props) => {
  const { active, ...rest } = props
  return (
    <chakra.a
      aria-current={active ? 'page' : undefined}
      w="full"
      my="37px"
      color="web"
      fontSize={["30px", "40px", "30px"]}
      fontFamily="body"
      display="flex"
      alignItems="center"
      justifyContent="center"
      fontWeight="500"
      {...rest}
    />
  )
}
// Fix hover states to match designs (use an arrow after the text)
const DesktopNavLink = React.forwardRef((props, ref) => {
  const { active, ...rest } = props
  return (
    <chakra.a
      ref={ref}
      fontSize={"18px"}
      fontWeight="700"
      aria-current={active ? 'page' : undefined}
      color={mode('web', 'cloud')}
      transition="all 0.3s"
      fontFamily="body"
      margin="0 auto"
      justifyContent={"center"}
      {...rest}
      _hover={{
        // color: 'gray.500',
        textDecor:"underline",
        textUnderlineOffset: "5px"
      }}
      _active={{
        color: 'blue.600',
        textDecor:'underline',
        textUnderlineOffset: "5px"
      }}
      _activeLink={{
        color: 'blue.600',
        fontWeight: 'bold',
        textDecor:'underline',
        textUnderlineOffset: "5px"
      }}
    />
  )
})

MobileNavLink.displayName = 'MobileNavLink'
DesktopNavLink.displayName = 'DesktopNavLink'

export const NavLink = {
  Mobile: MobileNavLink,
  Desktop: DesktopNavLink,
}
