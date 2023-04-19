import React, { ReactNode } from "react";

type InlineLogoProps = {
  logo: ReactNode;
  title: string;
};

const InlineLogo: React.FC<InlineLogoProps> = ({ logo, title }) => (
  <div style={{ display: "flex", paddingTop: 16 }}>
    {logo}
    <h1
      style={{ marginLeft: 12, marginTop: 2 }}
      className="nx-mt-2 nx-text-4xl nx-font-bold nx-tracking-tight nx-text-slate-900 dark:nx-text-slate-100"
    >
      {title}
    </h1>
  </div>
);

export default InlineLogo;
