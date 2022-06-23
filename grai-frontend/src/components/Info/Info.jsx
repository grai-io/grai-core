import React from 'react'
import {
  Box,
  Stack,
  Flex,
  Heading,
  Circle,
  Link,
  chakra
} from "@chakra-ui/react"
import { links } from './_data'
import {VendorSelections, Icons} from "./InfoIcons"
import Lottie from 'react-lottie'
import DesktopSplashAnimation from "../../images/diagram.json"
import MobileSplashAnimation from "../../images/diagramVertical.json"


export const DesktopDiagramAnimation = (props) => {
  const defaultOptions = {
      loop: true,
      autoplay: true,
      animationData: DesktopSplashAnimation,
      rendererSettings: {
        preserveAspectRatio: "xMidYMid slice"
      },
    };
  
  return (
    <Box
      {...props}
    >
      <Lottie 
        background="transparent"
	      options={defaultOptions}
        {...props}
      />
    </Box>
  );
}

export const MobileDiagramAnimation = (props) => {
  const defaultOptions = {
      loop: true,
      autoplay: true,
      animationData: MobileSplashAnimation,
      // rendererSettings: {
      //   preserveAspectRatio: "xMidYMid slice"
      // },
    };
  
  return (
    <Box
      {...props}
    >
      <Lottie 
        background="transparent"
	      options={defaultOptions}
        height={660}
      />
    </Box>
  );
}

export const InfoHeaders = (props) => {
  return (
    <Box
      {...props}
      as="section"
      bg="white"
      marginTop={{base: "30px", "md": "105px"}}
    >
      <chakra.a id={"nav-benefits"}>
        <Heading
          fontSize={{base: "16px", md: "24px"}}
          fontFamily={"body"}
          fontWeight={["700"]}
          textAlign={["center"]}
          lineHeight={["130%"]}
          color={"bastille"}
        >
          BENEFITS
        </Heading>        
      </chakra.a>

      <Heading
        fontSize={{base: "26px", md: "60px"}}
        fontFamily={"heading"}
        fontWeight={["700"]}
        textAlign={["center"]}
        lineHeight={["124%"]}
        marginX={"25px"}
        marginTop={{base: "11px", md: "31px"}}
        color={"bastille"}
      >
        Bring your data to life, with Grai.
      </Heading>
      <Box
        marginTop={{base: "20px", md: "100px"}}
      >

        <MobileDiagramAnimation 
          display={{base: "flex", md: "none"}}
        />
        
        <DesktopDiagramAnimation 
          display={{base: "none", md: "flex"}}
        />

        
      </Box>

    </Box>
  )
}

export const HowItWorks = (props) => {
  return (
    <Stack
      direction={{base: 'column', md: 'row'}}
      marginTop={{base: "35px", md: "52px"}}
      align="center"
      justify="space-between"
      px={[0, 10, 20]}
      maxW={"1440px"}
    >
      {
        links.map((link, idx) => {
          return (
            <Flex
            direction={["column"]}
            align={["center"]}
            justify={["center"]}
            w={["263px"]}
            key={"HowItWorks" + idx}
            >
              <link.icon
                h={["111px"]}
                w={["111px"]}
              >
              </link.icon>
              <Circle
                bg={link.bg}
                size={["31px"]}
                marginTop={["16px"]}
                color={"bastille"}
                alignItems={"center"}
                textAlign={"center"}
              >
                {idx+1}
              </Circle>
              <Box
                fontSize={{base: "26px", md: "24px"}}
                fontFamily={"heading"}
                lineHeight={{base: "32px", md: "30px"}}
                fontWeight={"bold"}
                marginTop="11px"
                color={"bastille"}
              >
                {link.header}
              </Box>
              <Box
                fontFamily={"body"}
                fontSize={{base: "16px", md: "18px"}}
                fontWeight={"500"}
                lineHeight={"130%"}
                marginTop={"11px"}
                color={"bastille"}
              >
                {link.text1}
              </Box>
              <Box
                fontFamily={"body"}
                fontSize={{base: "16px", md: "18px"}}
                lineHeight={"130%"}
                fontWeight={"500"}
                color={"bastille"}
                marginBottom={"35px"}
              >
                {link.text2}
              </Box>
            </Flex>
          )
        })
      }
      </Stack>
  )
}



export const Info = (props) => {
  const background = "linear-gradient(174.12deg, rgba(255, 255, 255, 0) 48.31%, rgba(245, 228, 234, 0.6006) 109.51%, #F1D7E0 193.01%)"
  return (
    <Box
      bg={background}
      align="center"
      {...props}
      >
      <InfoHeaders/>
      <Heading
        fontSize={{base: "26px", md: "34px"}}
        fontFamily={"heading"}
        fontWeight={["bold"]}
        textAlign={["center"]}
        lineHeight={{base: "32px", md: "42px"}}
        color={"bastille"}
        marginTop={{base: "75px", md:"100px"}}
        marginX = {{base: "26px"}}
      >
        Integrates with all the sources you already use.
      </Heading>
      <VendorSelections
        marginTop={{base: "35px", md: "40px"}}
        marginX = {{base: "26px"}}
      >
      </VendorSelections>
      <Icons
        w={{base: "86px", md: "144px"}}
        h={{base: "23px", md: "43px"}}
        marginX = {{base: "26px"}}
      >
      </Icons>
      <Heading
        fontSize={{base: "16px", md: "18px"}}
        fontFamily={"body"}
        fontWeight={["bold"]}
        textAlign={["center"]}
        lineHeight={{base: "22px", md: "24px"}}
        letterSpacing={["0.1em"]}
        color={"bastille"}
        marginTop={{base: "82px", md: "161px"}}
      >
        HOW IT WORKS
      </Heading>

      <HowItWorks/>
      
      <Flex
        display={{base: "none", md: "inherit"}}
      >
        <Flex
          align="center"
          justify="center"
          marginTop={"53px"}
          paddingBottom={"55px"}
        >
          <Link
          fontSize={"18px"}
          lineHeight={"24px"}
          fontFamily={"body"}
          fontWeight={"bold"}
          letterSpacing={"0.12px"}
          >
            Contact Us to Get Started →
          </Link>
        </Flex>
      </Flex>

    </Box>
  )
}