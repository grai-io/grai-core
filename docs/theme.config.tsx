import React from "react";
import { useState, useEffect } from "react";
import { DocsThemeConfig, useConfig } from "nextra-theme-docs";
import { useRouter } from "next/router";
import HeaderLogo from "./components/HeaderLogo";
import { Slack, Github } from "./components/Social";
import { FeedbackComponent } from "./components/Feedback";

const config: DocsThemeConfig = {
  project: {
    link: "https://github.com/grai-io/grai-core",
  },

  docsRepositoryBase: "https://github.com/grai-io/grai-core/tree/master/docs",
  useNextSeoProps() {
    const { frontMatter } = useConfig();
    return {
      titleTemplate: "%s – Grai",
      description: frontMatter.description || "Data lineage you can use",
    };
  },
  head: () => {
    const { asPath, defaultLocale, locale } = useRouter();
    const { frontMatter } = useConfig();
    return (
      <>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" href="/logo512.png" />
        <meta property="og:url" content={`https://docs.grai.io${asPath}`} />
        <meta property="og:title" content={frontMatter.title || "Nextra"} />
        <meta
          property="og:description"
          content={frontMatter.description || "The next site builder"}
        />
      </>
    );
  },
  darkMode: true,
  primaryHue: { dark: 265, light: 265 },
  logo: HeaderLogo,
  logoLink: "https://www.grai.io",

  main: ({ children }) => {
    return (
      <>
        {children}
        <FeedbackComponent contentSetId="e05b4f9f-0f68-4a1c-bcf3-5ceab9d4fa74" />
      </>
    );
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
  },
  footer: {
    text: (
      <span>
        Copyright © {new Date().getFullYear()}{" "}
        <a href="https://grai.io" target="_blank">
          Grai.io
        </a>
        .
      </span>
    ),
  },
  chat: {
    link: "https://join.slack.com/t/graicommunity/shared_invite/zt-1il70kfeb-TaCm5fwHg_quWCpKNYyj6w",
    icon: Slack,
  },

  banner: {
    key: "live-cloud", // key should be updated when the banner content changes
    dismissible: true,
    text: (
      <a href="https://grai.io" target="_blank">
        🎉 Grai cloud is now live. Read more →
      </a>
    ),
  },
  editLink: {
    text: "Edit this page on GitHub",
  },
  feedback: {
    useLink() {
      return "https://github.com/grai-io/grai-core/issues";
    },
  },
  navigation: {
    prev: true,
    next: true,
  },
  gitTimestamp({ timestamp }) {
    const [dateString, setDateString] = useState(timestamp.toISOString());

    useEffect(() => {
      setDateString(
        timestamp.toLocaleDateString(navigator.language, {
          day: "numeric",
          month: "long",
          year: "numeric",
        })
      );
    }, [timestamp]);

    return <>Last updated on {dateString}</>;
  },
  search: {
    component: undefined,
    placeholder: "Search Grai's Docs",
  },
};

export default config;
