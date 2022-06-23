import { RefObject } from "react";
export declare type UseAnimationStateProps = {
    isOpen: boolean;
    ref: RefObject<HTMLElement>;
};
export declare function useAnimationState(props: UseAnimationStateProps): {
    present: boolean;
    onComplete(): void;
};
//# sourceMappingURL=use-animation-state.d.ts.map