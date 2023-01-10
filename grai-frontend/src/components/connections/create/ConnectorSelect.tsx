import { InsertDriveFileOutlined } from "@mui/icons-material"
import React from "react"
import ConnectorList from "../connectors/ConnectorList"

const databases = [
  {
    title: "PostreSQL",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/245cb2ccbc976d6dc38d90456ca1fd7cdbcb2dc6-2424x2500.svg",
  },
  {
    title: "Snowflake",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/a4ac9f5f978ab2446fc17bf116067cb7c74116a2-960x952.png",
  },
  {
    title: "Amazon Redshift",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/f3e8edc5f92315c09202e01a28f206e777084c12-512x512.svg",
    disabled: true,
  },
  {
    title: "Google BigQuery",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/2a4f3d940e21dfa356bd993177586dab5e1b628f-2500x2500.svg",
    disabled: true,
  },
  {
    title: "Microsoft SQL Server",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/95bced9d0a4f668ceea0442a15c2cb4fdcb38b7e-452x452.png",
    disabled: true,
  },
  {
    title: "MongoDB",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/804ef5c917633c58b18f6cfc0d654b637cbc9a0e-128x128.png",
    disabled: true,
  },
  {
    title: "MySQL",
    iconSrc:
      "https://cdn.sanity.io/images/pwmfmi47/production/e4d7a37a2425ce7e012e23fdb4f53d985e18a4a3-1280x1280.png",
    disabled: true,
  },
]

const data_tools = [
  {
    title: "dbt",
    iconSrc: "/images/dbt-logo.png",
  },
  {
    title: "Fivetran",
    iconSrc: "/images/fivetran-logo.png",
  },
  {
    title: "Stitch",
    iconSrc: "/images/stitch-logo.png",
    disabled: true,
  },
]

const others = [
  {
    title: "Flat File",
    icon: <InsertDriveFileOutlined />,
  },
]

type ConnectorSelectProps = {
  onSelect: () => void
}

const ConnectorSelect: React.FC<ConnectorSelectProps> = ({ onSelect }) => {
  return (
    <>
      <ConnectorList
        title="Databases"
        connectors={databases}
        onSelect={onSelect}
      />
      <ConnectorList
        title="Data tools"
        connectors={data_tools}
        onSelect={onSelect}
      />
      <ConnectorList title="Other" connectors={others} onSelect={onSelect} />
    </>
  )
}

export default ConnectorSelect
