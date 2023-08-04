import React from "react";
import { useRouter } from "next/router";
import { FeelbackTaggedMessage, PRESET_LIKE_DISLIKE } from "@feelback/react";

export function FeedbackComponent({ contentSetId }: { contentSetId: string }) {
  const router = useRouter();

  return (
    <div className="feedback-wrap nx-border-t nx-pt-8 dark:nx-border-neutral-800 contrast-more:nx-border-neutral-400 dark:contrast-more:nx-border-neutral-400 print:nx-hidden">
      <FeelbackTaggedMessage key={router.route} // trick to reset state on page change
        contentSetId={contentSetId}
        layout="reveal-message"
        style="width-sm"
        preset={PRESET_LIKE_DISLIKE}
        title="Did this doc help you?"
        placeholder="Type the details (optional)"
        withEmail
        revokable={false}
        slots={{
          BeforeMessage: <p className="nx-text-xs nx-mt-4">Let us know the details</p>,
          BeforeEmail: <p className="nx-text-xs nx-mt-2">If we can contact you with more questions, please enter your email address</p>
        }}
      />
    </div>
  )
}
