import React from "react";
import { Link } from "@chakra-ui/react";

export const ExternalLink = ({ icon, href, ...rest }) => (
  <Link
    href={href}
    isExternal
    {...rest}
  >
    {icon}
  </Link>
);
