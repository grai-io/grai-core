// This file sets a custom webpack configuration to use your Next.js app
// with Sentry.
// https://nextjs.org/docs/api-reference/next.config.js/introduction
// https://docs.sentry.io/platforms/javascript/guides/nextjs/manual-setup/
const { withSentryConfig } = require("@sentry/nextjs");

const nextConfig = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
});


module.exports = nextConfig({
  // i18n doesn't work with static site generation
  // output: 'export',

  // i18n: {
  //   locales: ['en-US'],
  //   defaultLocale: 'en-US',
  //   domains: [
  //     {
  //       domain: "docs.grai.io",
  //       defaultLocale: "en-US",
  //     },
  //   ]
  // },
  images: {
    unoptimized: true,
  },
});


module.exports = withSentryConfig(
  module.exports,
  { silent: true },
  { hideSourceMaps: true }
);
