import * as React from 'react'
import Hero from '../components/Hero'
import Seo from '../components/seo'
import Info from '../components/Info'
import BenefitsSection from "../components/Benefits"
import CloserSection from "../components/Closer"

console.log(process.env)

const IndexPage = () => (
  <>
    <Seo title="Home" />
    <Hero paddingBottom={["90px"]}/>
    {/* <Stats paddingTop={["70px"]}/> */}
    <Info paddingTop={["45px"]}/>
    <BenefitsSection />
    {/* <IntegrationsSection /> */}
    <CloserSection />
  </>
);

export default IndexPage;
