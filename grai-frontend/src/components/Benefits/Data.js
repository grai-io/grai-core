import React from 'react'
import {
  InstantResultsIcon,
  IntegrationIcon,
  ValidationIcon,
  SilosIcon
} from "./Icons"

export const BenefitsData = [
  {
    label: 'SINGLE-CLICK VALUE',
    header: 'Get results instantly,  no code required',
    text: "You shouldn't need a team of PhD's to get started with machine learning and with Grai you won't. We make customer analytics as simple as clicking a button.",
    textColor: "bastille",
    icon: <InstantResultsIcon
      w={{base: "221px", md: "333px"}}
      h={{base: "310px", md: "467px"}}
    />,
    bg: 'white'
  },
  {
    label: 'AUTOMATIC INTEGRATION',
    header: 'Connect your data and let Grai integrate with your apps',
    text: "Grai automatically determines whether your data will work with an application and integrates the two for you.",
    textColor: "bastille",
    icon: <IntegrationIcon
    w={{base: "257px", md: "441px"}}
    h={{base: "268px", md: "460px"}}
    />,
    bg: 'polo'
  },
  {
    label: 'MODEL VALIDATION',
    header: 'Grai gives you facts, not fiction',
    text: 'Know exactly what apps are worth before clicking buy. Thanks to our automated integrations, all the information you need is available before making any commitments.',
    textColor: "bastille",
    icon: <ValidationIcon
      w={{base: "257px", md: "441px"}}
      h={{base: "268px", md: "460px"}}
    />,
    bg: 'white'
  },
  {
    label: 'NO SILOS',
    header: 'Grai works with your data, wherever it lives',
    text: 'Our collection of data integrations make connecting your data to apps fast and easy.',
    textColor: "white",
    icon: <SilosIcon
      w={{base: "257px", md: "441px"}}
      h={{base: "268px", md: "460px"}}
    />,
    bg: 'bastille'
  },
]