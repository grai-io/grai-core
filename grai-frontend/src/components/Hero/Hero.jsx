import React from 'react'
import {
  Box,
  Flex,
  LinkBox,
  LinkOverlay,
} from '@chakra-ui/react'
import Lottie from 'react-lottie'
import splashAnimation from "../../images/splash.json"


export const HeroAnimation = (props) => {
  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: splashAnimation,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice"
    },
  }
  
  return (
    <div>
      <Lottie 
        background="transparent"
	      options={defaultOptions}
        {...props}
      />
    </div>
  );
}

export const HeroMobile = (props) => {
  return (
    <Flex
      as="section"
      display={["flex"]}
      justifyContent={["center"]}
      direction="column"
      marginTop={"30px"}
      paddingBottom={"100px"}
      {...props}
    >

      <Box
        justify="center"
        align={"center"}
        fontFamily={"heading"}
        fontSize={{base:"42px"}}
        fontWeight={{base: "300"}}
        lineHeight={{base: "40px"}}
        color={"bastille"}
      >
        Your connection to
      </Box>
      <Box
        justify="center"
        align={"center"}
        fontFamily={"heading"}
        fontSize={{base:"42px"}}
        fontWeight={{base: "700"}}
        lineHeight={{base: "40px"}}
        color={"bastille"}
      >
        Machine Learning
      </Box>
      <Box
        justify="center"
        align={"center"}
        fontFamily={"body"}
        fontSize={{base:"16px"}}
        fontWeight={{base: "500"}}
        lineHeight={{base: "21px"}}
        marginTop={"19px"}
        color={"bastille"}
      >
        The fastest path to machine learning
      </Box>
      <Box
        justify="center"
        align={"center"}
        fontFamily={"body"}
        fontSize={{base:"16px"}}
        fontWeight={{base: "500"}}
        lineHeight={{base: "21px"}}
        color={"bastille"}

        marginBottom={"28px"}
      >
        and analytics.
      </Box>
        <LinkBox
            as='button'
            bg={['mango']} 
            w={["207px"]}
            h={["49px"]}
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
        <LinkBox
            as='button'
            bg={['transparent']} 
            w={["207px"]}
            h={["49px"]}
            m={["0 auto", null, "0"]}
            marginTop={"17px"}
            borderRadius={["0"]}
            borderColor={"bastille"}
            border={["1px"]}
          >
            <LinkOverlay href="#">
              <Box
                fontSize={["14px"]}
                fontWeight={["700"]}
                lineHeight={"19px"}
                color={"bastille"}
              >
                Explore the Grai App Store
              </Box>
              <Box
                fontSize={["14px"]}
                fontWeight={["700"]}
                lineHeight={"19px"}
                color={"bastille"}
              >
                (coming soon)
              </Box>
            </LinkOverlay>
          </LinkBox>

    </Flex>
  )
}

export const HeroDesktop = (props) => {
  return (

    <Flex
      as="section"
      justifyContent={["center"]}
      direction="column"
      marginTop={"30px"}
      paddingBottom={"80px"}
      {...props}
    >
      <Flex
        justify={"center"}
      >
        <HeroAnimation
        />
      </Flex>
      <Flex
        w={"100%"}
        position={"absolute"}
        direction={"column"}
        justifyContent={["center"]}
        alignItems={"center"}
        textAlign={"center"}

      >
        <Box
          justify="center"
          align={"center"}
          fontFamily={"heading"}
          fontSize={{base:"50px", md: "80px"}}
          fontWeight={{base: "300"}}
          lineHeight={{base: "95%"}}
          color={"bastille"}
        >
          Your connection to
        </Box>
        <Box
          justify="center"
          align={"center"}
          fontFamily={"heading"}
          fontSize={{base:"50px", md: "80px"}}
          fontWeight={{base: "700"}}
          lineHeight={{base: "95%"}}
          color={"bastille"}
        >
          Machine Learning
        </Box>
        <Box
          justify="center"
          align={"center"}
          fontFamily={"body"}
          fontSize={{base: "14px", md: "18px"}}
          fontWeight={{base: "500"}}
          lineHeight={{base: "130%"}}
          marginTop={"19px"}
          color={"bastille"}
        >
          The fastest path to machine learning and analytics.
        </Box>
        <Flex
          align={"center"}
          justify={"center"}
          direction={{base: "column", lg: "row"}}
          marginTop={{base: "28px", lg: "44px"}}
          columnGap={{"base": "17px"}}
        >
          <LinkBox
            as='button'
            bg={['mango']} 
            w={["152px"]}
            h={["55px"]}
            m={["0 auto"]}
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
          <LinkBox
            as='button'
            bg={['transparent']} 
            w={["236px"]}
            h={["55px"]}
            m={["0 auto"]}
            borderRadius={["0"]}
            borderColor={"bastille"}
            border={["1px"]}
          >
            <LinkOverlay href="/">
              <Box
                fontSize={["14px"]}
                fontWeight={["700"]}
                lineHeight={"19px"}
                color={"bastille"}
              >
                Explore the Grai App Store
              </Box>
              <Box
                fontSize={["14px"]}
                fontWeight={["700"]}
                lineHeight={"19px"}
                color={"bastille"}
              >
                (coming soon)
              </Box>
            </LinkOverlay>
          </LinkBox>
      </Flex>
      
      </Flex>
    </Flex>
  )
}


export const Hero = ({ siteTitle }) => {
  const bg = "linear-gradient(176.94deg, rgba(255, 255, 255, 0) -10.62%, rgba(255, 223, 189, 0.11913) 51.22%, rgba(255, 193, 127, 0.24168) 114.84%, rgba(255, 181, 103, 0.3) 145.12%)"
  return (
    <Box
      as="section"
    >
      <Box 
        className="hero-box" 
        height="100%"
        w="full"
        bg={bg}
      >
        <HeroMobile
          display={{
            base: "flex",
            md: "none",
          }}
        />
        <HeroDesktop
          display={{
            base: "none",
            md: "flex",
          }}
        />
      </Box>
    </Box>
  )
}