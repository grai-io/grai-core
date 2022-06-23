import React from 'react'
import {
  Box,
  Flex,
  Link,
  Text,
  LinkBox,
  LinkOverlay,
  useColorModeValue as mode,
} from "@chakra-ui/react"
import {
  FacebookIcon,
  InstagramIcon,

  YoutubeIcon,
  LogoFooter
} from "./Icons"

export const SocialsContainer = (props) => {
  return (
    <Flex
      {...props}
      maxW={["150px"]}
      mx={["auto", null, "0"]}
      gridColumnGap={[null, null, "40px"]}
      alignItems={["center"]}
      justifyContent={["space-between"]}
    >
      <FacebookIcon h={["20px"]} />
      <YoutubeIcon h={["20px"]} />
      <InstagramIcon h={["20px"]} />
    </Flex>
  )
}

export const FooterSocials = (props) => {
  const textColor = mode("web", "cloud")

  return (
    <Box
      display={[null, null, "none"]}
      py={["37px"]}
      {...props}
    >
      <Text
        fontWeight={["600"]}
        textAlign={["center"]}
        fontSize={["18px"]}
        marginBottom={["10px"]}
        color={textColor}
      >
        Follow us
      </Text>
      <SocialsContainer display={["flex", "flex", "none"]}/>
    </Box>
  )
}

export const CompanyInfo = (props) => {
  const lightMode = "linear-gradient(199.65deg, #FFFFFF -15.37%, #C1AAFD 270.4%), linear-gradient(95.79deg, #E45D33 -3.17%, #F2ACAA 145.44%)"
  const darkMode = "linear-gradient(89.47deg, #372D56 37.51%, #C1AAFD 186.21%)"
  const bg = mode(lightMode, darkMode)
  const textColor = mode("web", "cloud")

  return (
    <Flex
      justify={["center", null, "space-between"]}
      bg={bg}
      fontWeight={["600"]}
      py={["32px"]}
      px={[null, null, "40px"]}
    >
      <Text
        textAlign={["center"]}
        m={["0"]}
        color={textColor}
      >
        © {new Date().getFullYear()} {props.companyName}
      </Text>
      <SocialsContainer display={["none", "none", "flex"]}/>
    </Flex>
  )
}

export const FooterItems = (props) => {
  const color = "#FFFFFF"
  return (
      <Flex
        direction={["column", null, null,  "row-reverse"]}
        justify={["center", null, "space-between"]}
        marginTop={["30px", null, null, "0"]}
        align={[null, null, "center"]}
        gridColumnGap={[null, null, "33px"]}
        h={["inherit"]}
      >
        <LinkBox
          as='button'
          bg={['mango']} 
          w={["300px", null, null, "152px"]}
          h={["48px", null, null, "40px"]}
          m={["0 auto", null, "0"]}
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
        <Flex
          fontWeight={["500"]}
          fontSize={["16px"]}
          color={[color]}
          justify={["space-between", "space-between", "center"]}
          direction={["column", null, null, "row"]}
          gridColumnGap={["25px"]}
          gridRowGap={["20px"]}
          align={["center"]}
          marginTop={["30px", null, null, "0"]}
        >
    
        <Link href="#nav-benefits">
          Benefits
        </Link>

        <Link href="/dev">
          For Developers
        </Link>

        <Link href="https://github.com/grai-io">
          Documentation
        </Link>

        <Link href="mailto:sales@grai.io">
          Contact
        </Link>

        <Link href="https://github.com/grai-io">
          Github
        </Link>

      </Flex>
      </Flex>
  )
}

export const Footer = (props) => {
  const bg = "#351D36"
  return (
    <Flex
    as={"footer"}
    // h={["192px"]}
    w={["100%"]}
    bg={bg}
    flexDirection={["column", null, null,  "row"]}
    paddingTop={["64px"]}
    paddingBottom={["48px"]}
    align={["center"]}
    justify={[null, null, "space-between"]}
    px={[null, null, "40px"]}
    >
      {/* <Box w={["22.64%"]}> */}
      <LogoFooter
        w={["104px"]}
        h={["92px"]}
        mx={["auto", null, "0"]}
        //marginBottom={["42.56px"]}
      />      
      {/* </Box> */}
      <FooterItems 
     
      />  

      
      {/* <FooterSocials /> */}
      {/* <CompanyInfo companyName={"Grai.io Inc."} /> */}
    </Flex>
  )
}
