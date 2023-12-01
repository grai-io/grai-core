import React, { ReactNode } from "react";
import Image from "next/image";

type InlineLogoProps = {
  logo: ReactNode;
  title: string;
};

const InlineLogo: React.FC<InlineLogoProps> = ({ logo, title }) => (
  <div style={{ display: "flex", alignItems: "center", paddingTop: 16 }}>
    {logo}
    <h1
      style={{ marginLeft: 12 }}
      className="nx-mt-2 nx-text-4xl nx-font-bold nx-tracking-tight nx-text-slate-900 dark:nx-text-slate-100"
    >
      {title}
    </h1>
  </div>
);
export default InlineLogo;


type InlineImageTextProps = {
  src: string;
  text: string;
  alt: string;
  height: number;
  width: number;
};


const InlineImageText: React.FC<InlineImageTextProps>  = ({ src, text, height, width }) => (
  <div style={{ display: 'flex', alignItems: 'center' }}>
    <Image
      src={src}
      height={height ? height : 120}
      width={width ? width : 120}
      alt={"Inline image for " + text}
    />
    <h1
      style={{ marginLeft: 12 }}
      className="nx-mt-2 nx-text-4xl nx-font-bold nx-tracking-tight nx-text-slate-900 dark:nx-text-slate-100"
    >
      {text}
    </h1>
  </div>
)

export {
  InlineLogo,
  InlineImageText
};
