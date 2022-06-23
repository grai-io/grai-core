declare type InitFn<T> = () => T;
/**
 * Creates a constant value over the lifecycle of a component.
 *
 * Even if `useMemo` is provided an empty array as its final argument, it doesn't offer
 * a guarantee that it won't re-run for performance reasons later on. By using `useConst`
 * you can ensure that initializers don't execute twice or more.
 */
export declare function useConst<T extends any>(init: T | InitFn<T>): T;
export {};
//# sourceMappingURL=use-const.d.ts.map