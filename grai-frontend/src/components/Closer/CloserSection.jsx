import React from 'react'
import {
  Box,
  Flex,
  Button,
} from '@chakra-ui/react'
import {
  DesktopLeftIcon,
  DesktopRightIcon,
  MobileBottomLeftIcon,
  MobileBottomRightIcon,
  MobileTopLeftIcon,
  MobileTopRightIcon
} from "./Icons"


export const CloserSectionMobile = (props) => {
  return (
    <Flex
      as="section"
      
      direction={"column"}
      {...props}
    >
      <Flex
        marginTop={"32px"}
        flexWrap={"wrap"}
        justifyContent={"space-between"}
      >
        <MobileTopLeftIcon
          w={{base: "92px"}}
          h={{base: "91px"}}
          position={"relative"}
          left={"20px"}
        />

        <MobileTopRightIcon
          w={{base: "136px"}}
          h={{base: "78px"}}
          position={"relative"}
          right={"13px"}
        />
      </Flex>
      <Flex
        marginTop={"25px"}
        justify={"center"}
        align={"center"}
        direction={"column"}
      >
        <Flex
          align="center"
          justify="center"
          color={'bastille'}
          fontFamily={"heading"}
          fontWeight={"700"}
          fontSize={{base: "42px"}}
          lineHeight={{base: "40px"}}
        >
          Put your data
        </Flex>
        <Flex
          align="center"
          justify="center"
          color={'bastille'}
          fontFamily={"heading"}
          fontWeight={"700"}
          fontSize={{base: "42px"}}
          lineHeight={{base: "40px"}}
        >
          to work
        </Flex>
        <Button 
            fontSize={["med"]}
            fontWeight={["700"]}
            // justifySelf={"center"}
            bg={['mango']} 
            w={{base: "133px"}}
            h={{base: "70"}}
            borderRadius={["0"]}
            border={["1px"]}
            marginTop={"20px"}
          >
            Get Started
          </Button>

        <Flex
          justify={"space-between"}
          w={"100%"}
          position={"relative"}
        >
          <MobileBottomLeftIcon
            w={{base: "118px"}}
            h={{base: "91px"}}
            position={"relative"}
            top={"-24px"}
            left={"-20px"}
          />   
          <MobileBottomRightIcon
            w={{base: "136px"}}
            h={{base: "78px"}}
            position={"relative"}
            bottom={"24px"}
            right={"-22px"}
          />
        </Flex>
      </Flex>
    </Flex>
  )
}

export const CloserSectionDesktop = (props) => {
  
  const marginTop = {base: "62px", md: "40px"}
  return (
    <Flex
      as="section"
      direction={"row"}
      paddingTop={marginTop}
      justify={"space-between"}
      {...props}
    >
      <Flex
        h={"384px"}
        w={"263px"}
      >
        <DesktopLeftIcon/>
      </Flex>
      <Flex
        justify={"center"}
        align={"center"}
        direction={"column"}
      >
        <Flex
          textAlign="center"
          justify="center"
          color={'bastille'}
          fontFamily={"heading"}
          fontWeight={"700"}
          fontSize={{base: "60px", xl: "80px"}}
          lineHeight={{base: "95%"}}
        >
          Put your data to work
        </Flex>

        <Button 
          fontSize={["med"]}
          fontWeight={["700"]}
          // justifySelf={"center"}
          bg={['mango']} 
          w={{base: "133px"}}
          h={{base: "48px"}}
          borderRadius={["0"]}
          border={["1px"]}
          marginTop={"20px"}
        >
          Get Started
        </Button>
      </Flex>
      <Flex
        h={"379px"}
        w={"295px"}
        justify={"flex-end"}
        position={"relative"}
      >
        <DesktopRightIcon/>
      </Flex>
    </Flex>
  )
}

export const CloserSection = (props) => {
  const bg = "linear-gradient(356.94deg, rgba(255, 255, 255, 0) -10.62%, rgba(255, 223, 189, 0.3971) 51.22%, rgba(255, 193, 127, 0.8056) 114.84%, #FFB567 145.12%)"
  return (
       <Box 
      className="closer-box" 
      height="100%"
      m="auto 0"
      bg={bg}
    >
      <CloserSectionMobile
        display={{
          base: "flex",
          md: "none",
        }}
      />
      <CloserSectionDesktop
        display={{
          base: "none",
          md: "flex",
        }}
      />
    </Box>
  )
}