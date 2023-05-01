export default {
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://docs.grai.io/",
    siteName: "Grai Docs",
  },
  twitter: {
    handle: "@Grai_io",
    site: "@Grai_io",
    cardType: "summary_large_image",
  },
  languageAlternates:[{
    hrefLang: 'en-US',
    href: process.env.WEB_URI,
  }]
};
