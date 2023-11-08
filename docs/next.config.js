// This file sets a custom webpack configuration to use your Next.js app
// with Sentry.
// https://nextjs.org/docs/api-reference/next.config.js/introduction
// https://docs.sentry.io/platforms/javascript/guides/nextjs/manual-setup/
const { withSentryConfig } = require("@sentry/nextjs");
const redirects = require('./redirects');

const nextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
});

const nextConfig = {
  images: {
    unoptimized: false,
  },

  async redirects() {
    return redirects;
  },
};

const nextraConfig = nextra(nextConfig);

const sentryConfig = withSentryConfig(nextraConfig, {
  silent: true,
  hideSourceMaps: false,
});

module.exports = sentryConfig;
