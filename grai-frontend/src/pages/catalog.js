import * as React from 'react'
import Seo from '../components/seo'
import Catalog from '../components/Catalog'
import Footer from "../components/Footer"

const CatalogPage = () => (
  <>
    <Seo title="catalog" />
    <Catalog />
  </>
)

export default CatalogPage