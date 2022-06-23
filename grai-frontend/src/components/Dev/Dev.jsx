import React from 'react'
import {
  Box,
  Flex,
  Button,
  VStack,
  Stack,
  Text,
  SimpleGrid,
  GridItem,
  FormLabel,
  FormHelperText,
  FormControl,
  Input,
  LinkBox,
  LinkOverlay
} from '@chakra-ui/react'
import {SignupForm} from '../Signup/SignupForm'

export const backgroundColor = "kobilight"
export const LeftMargins = {base: "25px", md: "100px"}

export const ContactButtons = (props) => {
  const buttonWidth = {base: "148px", md: "180px" }
  const buttonHeight = {base: "61px", md: "74px"}
  const buttonText ={
    color: "bastille",
    fontSize: {base: "14px", md: "16px"},
    lineHeight: "135%",
    letterSpacing: {base: "0.17px", md: "0.2px"},
    fontWeight: "700"
  }
  return (
    <Flex
      marginTop={{base: "35px"}}

    >
      {/* <Button
        borderRadius={["0"]}
        border={"1px"}
        w={buttonWidth}
        h={buttonHeight}
        bg={"mango"}
        href={"mailto:sales@grai.io"}
      >
        <Box
          direction="column"
          align="left"
        >
          <Box>Email us</Box>
          <Box>sales@grai.io</Box>   
        </Box>

      </Button> */}
      <LinkBox
        as='button'
        borderRadius={["0"]}
        border={"1px"}
        w={buttonWidth}
        h={buttonHeight}
        bg={"mango"}
      >
        <LinkOverlay href="mailto:dev@grai.io">
          <Box
            direction="column"
            align="left"
            marginLeft={{base:"16px", md:"20px"}}
          >
            <Text {...buttonText} >Email us</Text>
            <Text {...buttonText} >dev@grai.io</Text>
          </Box>
        </LinkOverlay>

      </LinkBox>
      <LinkBox
        as='button'
        borderRadius={["0"]}
        border={"1px"}
        w={buttonWidth}
        h={buttonHeight}
        marginLeft={{base:"12px", md:"30px"}}
      >
        <LinkOverlay href="#">
          <Box
            direction="column"
            align="left"
            marginLeft={{base:"16px", md:"20px"}}
          >
            <Text {...buttonText} >Call us</Text>
            <Text {...buttonText} >(coming soon)</Text>
          </Box>
        </LinkOverlay>
      </LinkBox>
    </Flex>
  )
}

export const WaitingListGreeting = (props) => {
  
  return (
    <VStack
      // w="50%"
      h="full"
      marginTop={{base: "50px", lg: "115px"}}
      // marginBottom={{base: "52px", md: "145px"}}
      align={"flex-start"}
      marginLeft={{base: "25px", lg: "100px"}}
      spacing="24px"
    >
      <Box
        fontFamily="body"
        fontSize={{base: "14px", lg: "18px"}}
        color={"bastille"}
        fontWeight={"bold"}
        lineHeight={"135%"}
        letterSpacing={"0.1em"}
        textTransform={"uppercase"}
      >
        Grai for developers
      </Box>
      <VStack align="flex-start">
        <Box
          fontFamily="heading"
          fontSize={{base: "40px", lg: "70px"}}
          color={"bastille"}
          fontWeight={"bold"}
          lineHeight={"124%"}
        >
          Ready to build
        </Box>
        <Box

          fontFamily="heading"
          fontSize={{base: "40px", lg: "70px"}}
          color={"bastille"}
          fontWeight={"bold"}
          lineHeight={"124%"}
        >
          with Grai?
        </Box>
      </VStack>

      <Box
          fontFamily="body"
          fontSize={{base: "14px", lg: "18px"}}
          color={"bastille"}
          lineHeight={"130%"}
          marginTop={{base: "35px"}}
      >
        Sign up here or contact us at:
      </Box>
      <ContactButtons />
      

    </VStack>
  )
}

export const DevSignup = (props) => {
  return (
    <Flex
      bg={backgroundColor}
      justify="space-between"
    >
      <Stack
        direction={{base: "column", lg: "row"}}
      >
        <Flex
          marginBottom={{base: "0px", lg: "145px"}}
          w="60%"
        >
          <WaitingListGreeting/>
        </Flex>
        <Flex
          // w="full"
          h="full"
          paddingX={{base: "25px", lg: "80px"}}
          marginLeft="auto"
          paddingY={{base: "52px", lg: "55px"}}
        >
          <SignupForm location='dev'/>
        </Flex>
      </Stack>
    </Flex>
  )
}
