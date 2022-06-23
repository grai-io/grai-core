import React from 'react'
import {
  Box,
  Flex,
  VStack,
  Stack,
  Text,
  LinkBox,
  LinkOverlay
} from '@chakra-ui/react'

import {SignupForm} from './SignupForm'

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

      <LinkBox
        as='button'
        borderRadius={["0"]}
        border={"1px"}
        w={buttonWidth}
        h={buttonHeight}
        bg={"mango"}
      >
        <LinkOverlay href="mailto:sales@grai.io">
          <Box
            direction="column"
            align="left"
            marginLeft={{base:"16px", md:"20px"}}
          >
            <Text {...buttonText} >Email us</Text>
            <Text {...buttonText} >sales@grai.io</Text>
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

// export const SignupForm = (props) => {
//   const baseStyle = {
//     color: {base: "bastille"},
//     fontFamily: "heading",
//     fontSize: {base: "16px", lg: "15px"},
//     fontWeight: "500",
//     lineHeight: "135%"
//   }
//   const gridWidths = {base: 4, lg: 2}
//   return (
//     <Flex
//       bg="pololight"
//       w="full"
//       h="full"
//       px={{base: "18px", lg: "35px"}}
//       py={{base: "35px", lg: "49px"}}
//       border={"1px"}

//     >
//       <SimpleGrid 
//         columns={4}
//         columnGap={{base: "0 auto", lg: "26px"}}
//         rowGap={{base: "32px", lg: "32px"}}
//       >
//         <GridItem colSpan={gridWidths}>
//           <FormControl isRequired>
//             <FormLabel {...baseStyle}> First Name </FormLabel>
//             <Input placeholder='Tommy' bg='white' />
//           </FormControl>
//         </GridItem>
//         <GridItem colSpan={gridWidths}>
//           <FormControl isRequired>
//             <FormLabel {...baseStyle}>Last Name</FormLabel>
//             <Input placeholder='Tutone' bg='white' />
//           </FormControl>
//         </GridItem>
//         <GridItem colSpan={4}>
//           <FormControl>
//             <FormLabel {...baseStyle}>Company Name</FormLabel>
//             <Input placeholder='Columbia Records' bg='white' />
//           </FormControl>
//         </GridItem>
//         <GridItem colSpan={gridWidths}>
//           <FormControl isRequired>
//             <FormLabel {...baseStyle}>Email Address</FormLabel>
//             <Input placeholder='tommy.tutone@gmail.com' bg='white' />
//           </FormControl>
//         </GridItem>
//         <GridItem colSpan={gridWidths}>
//           <FormControl>
//             <FormLabel {...baseStyle}>Phone Number</FormLabel>
//             <Input placeholder='+1 (314) 867-5309' bg='white' />

//           </FormControl>
//         </GridItem>
//         <GridItem colSpan={{base: 2, lg: 1}}>
//           <Button
//             size="lg"
//             borderRadius={["0"]}
//             border={"1px"}
//             bg="mango"
//             w="full"
//             loadingText='Submitting'
//             spinnerPlacement='start'
//           >
//             Join
//           </Button>
//         </GridItem>
//       </SimpleGrid>


//     </Flex>
//   )

// }

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
        Grai for business
      </Box>
      <VStack align="flex-start">
        <Box
          fontFamily="heading"
          fontSize={{base: "40px", lg: "70px"}}
          color={"bastille"}
          fontWeight={"bold"}
          lineHeight={"124%"}
        >
          Join the
        </Box>
        <Box

          fontFamily="heading"
          fontSize={{base: "40px", lg: "70px"}}
          color={"bastille"}
          fontWeight={"bold"}
          lineHeight={"124%"}
        >
          Waiting List
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



export const Signup = (props) => {
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
        >
          <WaitingListGreeting/>
        </Flex>
        <Flex
          w="full"
          h="full"
          paddingX={{base: "25px", lg: "80px"}}
          marginLeft="auto"
          paddingY={{base: "52px", lg: "55px"}}
        >
          <SignupForm location='customer'/>
        </Flex>
      </Stack>
    </Flex>
  )
}
