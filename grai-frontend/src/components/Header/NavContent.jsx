import {
  Box,
  Flex,
  Stack,
  IconButton,
  useDisclosure,
  LinkBox,
  LinkOverlay,
} from '@chakra-ui/react'
import * as React from 'react'
import { NavLink } from './NavLink'
import { NavMenu } from './NavMenu'
import { MobileIcons } from './NavIcons'
import { links } from './_data'
import { Logo, MobileLogo } from './Logo'

const MobileNavContext = (props) => {
  const { isOpen, onToggle } = useDisclosure()
  
  return (
    <>
      <Flex
        {...props}
        h="100%"

        align="center"
        justify="space-between"
        className="nav-content__mobile"
        marginTop={"37px"}
        paddingBottom={"34px"}
        borderBottom={["1px"]}
        borderColor={["bastille"]}
      >
        <Box as="a" rel="home" href="/">
          <MobileLogo
            h={{base:"48px"}}
            w={{base: "48px"}}
            marginLeft={{base: "25px"}}
          />
        </Box>
        <Flex align="center">
          <LinkBox
            as='button'
            bg={['mango']} 
            w={["105px"]}
            h={["41px"]}
            m={["18px"]}
            borderRadius={["0"]}
            borderColor={"bastille"}
            border={["1px"]}
          >
            <LinkOverlay href="/signup">
              <Box
                fontSize={["14px"]}
                fontWeight={["700"]}
                lineHeight={"19px"}
                color={"bastille"}
              >
                Get Started
              </Box>
            </LinkOverlay>
          </LinkBox>
          <IconButton
            display={{
              base: 'flex',
              lg: 'none',
            }}
            size="sm"
            mr={"25px"}
            alignItems='center'
            aria-label="Open menu"
            variant="unstyled"
            onClick={onToggle}
            icon={isOpen ? <MobileIcons.CloseIcon w="20px"/> : <MobileIcons.HamburgerIcon w="30px"/>} />
        </Flex>
      </Flex>
      <NavMenu animate={isOpen ? 'open' : 'closed'} zIndex={9000}>
        {links.map((link, idx) => {
            if (link.label === 'Github') {
             return (
               <NavLink.Mobile 
                key={"NavContentMobile" + idx} 
                href={link.href}
              >
                {<MobileIcons.GithubIcon 
                  w="54px" 
                  h="53px" 
                  m="margin-bottom: 37px" 
                  fill={"mango"}
                />}
              </NavLink.Mobile>
             )
            } else {
              return (
                <NavLink.Mobile 
                  key={"NavContentMobile" + idx} 
                  href={link.href}
                  color="mango"
                >
                  {link.label}
                </NavLink.Mobile>
              )
            }
        })}
      </NavMenu>
    </>
  )
}

const DesktopNavContent = (props) => {
  const fontSize = "18px"
  const fontWeight = "500"

  return (
    <Flex
      className="nav-content__desktop"
      align="center"

      justifyContent="space-between"
      {...props}
      borderBottom={["1px"]}
      borderColor={["bastille"]}
      h={"78px"}
    >
      <Flex as="a" href="/" rel="home" alignItems="center">
        <Logo 
          w={"165px"}
          marginLeft={["50px"]}
        >
        </Logo>
      </Flex>
      <Stack
        direction="row"
        as="ul"
        id="nav__primary-menu"
        aria-label="Main Menu"
        listStyleType="none"
        gridColumnGap="39px"
        marginLeft={["auto"]}
        h="100%"
        align="center"
        justify="center"
        justifyContent="center"
        alignItems={"center"}
      >
        {links.map((link, idx) => {
          if (link.label === 'Github') {
            return (
              <Flex
                as="li"
                key={"navContent" + idx}
                id={`nav__menuitem-${idx}`}
                mx={["0"]}
              >
                <NavLink.Desktop  href={link.href}>
                  {<MobileIcons.GithubIcon
                    w={["25px"]}
                    h={["24px"]} />}
                </NavLink.Desktop>
              </Flex>
            )
          } else if (link.label === "Get Started") {
            return (
              <Flex 
                as="li" 
                key={idx} 
                id={`nav__menuitem-${idx}`}
                fontSize={[fontSize]}
                fontWeight={[fontWeight]}
                lineHeight={"20px"}
                borderRadius={["0"]}
                borderLeft={"1px"}
                borderColor={"bastille"}
                bg={['mango']}
                color="bastille"
                h="100%"
                w={"235px"}
                align="center"
              >
                <NavLink.Desktop 
                  href={link.href}
                  alignItems="center"
                >
                  {link.label}
                </NavLink.Desktop>
              </Flex>
            )
          } else {
            return (
              <Flex 
                as="li" 
                key={idx} 
                id={`nav__menuitem-${idx}`}
                fontSize={[fontSize]}
                lineHeight={"24px"}
                fontWeight={"700"}

              >
                <NavLink.Desktop href={link.href}>
                  {link.label}
                </NavLink.Desktop>
              </Flex>
  
            )
          }
        })}
      </Stack>
      {/* <Button 
        fontSize={["med"]}
        fontWeight={[fontWeight]}
        bg={['mango']} 
        w={["300px", null, null, "235px"]}
        color="bastille"
        fontSize={"18px"}
        lineHeight={"20px"}
        fontWeight={"700"}
        h={["100%"]}
        // m={["0 auto", null, "0"]}
        borderRadius={["0"]}
        borderLeft={"1px"}
        borderColor={"bastille"}
      >
        Get Started
      </Button> */}
    </Flex>
  )
}

export const NavContent = {
  Mobile: MobileNavContext,
  Desktop: DesktopNavContent,
}
