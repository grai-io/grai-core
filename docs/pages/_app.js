import { useEffect } from "react";
import { useRouter } from "next/router";
import { DefaultSeo } from 'next-seo';
import SEO from '../next-seo.config';

import posthog from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import { MendableFloatingButton } from '@mendable/search';


const MendableSearch = () => {
  return (
    <MendableFloatingButton
      // style={{darkMode:false, accentColor: "#ffffff"}}
      dialogPlaceholder="What are you looking for?"
      anon_key={"0b8c6a95-5bfe-4d8e-99ac-c8d3877d4c70"}
      showSimpleSearch={true}
      // floatingButtonStyle={{
      //   backgroundColor: "#6e17e8",
      //   color: "#ffb567",
      // }}
      // icon={""}
      messageSettings={{
          prettySources: true,
      }}
    />
  );
};

// Check that PostHog is client-side (used to handle Next.js SSR)
if (typeof window !== "undefined") {
  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://app.posthog.com",
    // Enable debug mode in development
    loaded: (posthog) => {
      if (process.env.NODE_ENV === "development") posthog.debug();
    },
  });
}

export default function App({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    // Track page views
    const handleRouteChange = () => posthog?.capture("$pageview");
    router.events.on("routeChangeComplete", handleRouteChange);

    return () => {
      router.events.off("routeChangeComplete", handleRouteChange);
    };
  }, []);

  // return the component with a PostHog provider and SEO
  return (
      <PostHogProvider client={posthog}>
        <DefaultSeo {...SEO} />
        <MendableSearch />
        <Component {...pageProps} />
      </PostHogProvider>
  );
}
