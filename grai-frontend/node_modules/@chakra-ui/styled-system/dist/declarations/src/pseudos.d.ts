export declare const pseudoSelectors: {
    /**
     * Styles for CSS selector `&:hover`
     */
    _hover: string;
    /**
     * Styles for CSS Selector `&:active`
     */
    _active: string;
    /**
     * Styles for CSS selector `&:focus`
     *
     */
    _focus: string;
    /**
     * Styles for the highlighted state.
     */
    _highlighted: string;
    /**
     * Styles to apply when a child of this element has received focus
     * - CSS Selector `&:focus-within`
     */
    _focusWithin: string;
    /**
     * Styles to apply when this element has received focus via tabbing
     * - CSS Selector `&:focus-visible`
     */
    _focusVisible: string;
    /**
     * Styles to apply when this element is disabled. The passed styles are applied to these CSS selectors:
     * - `&[aria-disabled=true]`
     * - `&:disabled`
     * - `&[data-disabled]`
     */
    _disabled: string;
    /**
     * Styles for CSS Selector `&:readonly`
     */
    _readOnly: string;
    /**
     * Styles for CSS selector `&::before`
     *
     * NOTE:When using this, ensure the `content` is wrapped in a backtick.
     * @example
     * ```jsx
     * <Box _before={{content:`""` }}/>
     * ```
     */
    _before: string;
    /**
     * Styles for CSS selector `&::after`
     *
     * NOTE:When using this, ensure the `content` is wrapped in a backtick.
     * @example
     * ```jsx
     * <Box _after={{content:`""` }}/>
     * ```
     */
    _after: string;
    /**
     * Styles for CSS selector `&:empty`
     */
    _empty: string;
    /**
     * Styles to apply when the ARIA attribute `aria-expanded` is `true`
     * - CSS selector `&[aria-expanded=true]`
     */
    _expanded: string;
    /**
     * Styles to apply when the ARIA attribute `aria-checked` is `true`
     * - CSS selector `&[aria-checked=true]`
     */
    _checked: string;
    /**
     * Styles to apply when the ARIA attribute `aria-grabbed` is `true`
     * - CSS selector `&[aria-grabbed=true]`
     */
    _grabbed: string;
    /**
     * Styles for CSS Selector `&[aria-pressed=true]`
     * Typically used to style the current "pressed" state of toggle buttons
     */
    _pressed: string;
    /**
     * Styles to apply when the ARIA attribute `aria-invalid` is `true`
     * - CSS selector `&[aria-invalid=true]`
     */
    _invalid: string;
    /**
     * Styles for the valid state
     * - CSS selector `&[data-valid], &[data-state=valid]`
     */
    _valid: string;
    /**
     * Styles for CSS Selector `&[aria-busy=true]` or `&[data-loading=true]`.
     * Useful for styling loading states
     */
    _loading: string;
    /**
     * Styles to apply when the ARIA attribute `aria-selected` is `true`
     *
     * - CSS selector `&[aria-selected=true]`
     */
    _selected: string;
    /**
     * Styles for CSS Selector `[hidden=true]`
     */
    _hidden: string;
    /**
     * Styles for CSS Selector `&:-webkit-autofill`
     */
    _autofill: string;
    /**
     * Styles for CSS Selector `&:nth-child(even)`
     */
    _even: string;
    /**
     * Styles for CSS Selector `&:nth-child(odd)`
     */
    _odd: string;
    /**
     * Styles for CSS Selector `&:first-of-type`
     */
    _first: string;
    /**
     * Styles for CSS Selector `&:last-of-type`
     */
    _last: string;
    /**
     * Styles for CSS Selector `&:not(:first-of-type)`
     */
    _notFirst: string;
    /**
     * Styles for CSS Selector `&:not(:last-of-type)`
     */
    _notLast: string;
    /**
     * Styles for CSS Selector `&:visited`
     */
    _visited: string;
    /**
     * Used to style the active link in a navigation
     * Styles for CSS Selector `&[aria-current=page]`
     */
    _activeLink: string;
    /**
     * Used to style the current step within a process
     * Styles for CSS Selector `&[aria-current=step]`
     */
    _activeStep: string;
    /**
     * Styles to apply when the ARIA attribute `aria-checked` is `mixed`
     * - CSS selector `&[aria-checked=mixed]`
     */
    _indeterminate: string;
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is hovered
     */
    _groupHover: string;
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is hovered
     */
    _peerHover: string;
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is focused
     */
    _groupFocus: string;
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is focused
     */
    _peerFocus: string;
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` has visible focus
     */
    _groupFocusVisible: string;
    /**
     * Styles to apply when a sibling element with `.peer`or `data-peer` has visible focus
     */
    _peerFocusVisible: string;
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is active
     */
    _groupActive: string;
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is active
     */
    _peerActive: string;
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is disabled
     */
    _groupDisabled: string;
    /**
     *  Styles to apply when a sibling element with `.peer` or `data-peer` is disabled
     */
    _peerDisabled: string;
    /**
     *  Styles to apply when a parent element with `.group`, `data-group` or `role=group` is invalid
     */
    _groupInvalid: string;
    /**
     *  Styles to apply when a sibling element with `.peer` or `data-peer` is invalid
     */
    _peerInvalid: string;
    /**
     * Styles to apply when a parent element with `.group`, `data-group` or `role=group` is checked
     */
    _groupChecked: string;
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` is checked
     */
    _peerChecked: string;
    /**
     *  Styles to apply when a parent element with `.group`, `data-group` or `role=group` has focus within
     */
    _groupFocusWithin: string;
    /**
     *  Styles to apply when a sibling element with `.peer` or `data-peer` has focus within
     */
    _peerFocusWithin: string;
    /**
     * Styles to apply when a sibling element with `.peer` or `data-peer` has placeholder shown
     */
    _peerPlaceholderShown: string;
    /**
     * Styles for CSS Selector `&::placeholder`.
     */
    _placeholder: string;
    /**
     * Styles for CSS Selector `&:placeholder-shown`.
     */
    _placeholderShown: string;
    /**
     * Styles for CSS Selector `&:fullscreen`.
     */
    _fullScreen: string;
    /**
     * Styles for CSS Selector `&::selection`
     */
    _selection: string;
    /**
     * Styles for CSS Selector `[dir=rtl] &`
     * It is applied when a parent element or this element has `dir="rtl"`
     */
    _rtl: string;
    /**
     * Styles for CSS Selector `[dir=ltr] &`
     * It is applied when a parent element or this element has `dir="ltr"`
     */
    _ltr: string;
    /**
     * Styles for CSS Selector `@media (prefers-color-scheme: dark)`
     * It is used when the user has requested the system use a light or dark color theme.
     */
    _mediaDark: string;
    /**
     * Styles for CSS Selector `@media (prefers-reduced-motion: reduce)`
     * It is used when the user has requested the system to reduce the amount of animations.
     */
    _mediaReduceMotion: string;
    /**
     * Styles for when `data-theme` is applied to any parent of
     * this component or element.
     */
    _dark: string;
    /**
     * Styles for when `data-theme` is applied to any parent of
     * this component or element.
     */
    _light: string;
};
export declare type Pseudos = typeof pseudoSelectors;
export declare const pseudoPropNames: ("_hover" | "_active" | "_focus" | "_highlighted" | "_focusWithin" | "_focusVisible" | "_disabled" | "_readOnly" | "_before" | "_after" | "_empty" | "_expanded" | "_checked" | "_grabbed" | "_pressed" | "_invalid" | "_valid" | "_loading" | "_selected" | "_hidden" | "_autofill" | "_even" | "_odd" | "_first" | "_last" | "_notFirst" | "_notLast" | "_visited" | "_activeLink" | "_activeStep" | "_indeterminate" | "_groupHover" | "_peerHover" | "_groupFocus" | "_peerFocus" | "_groupFocusVisible" | "_peerFocusVisible" | "_groupActive" | "_peerActive" | "_groupDisabled" | "_peerDisabled" | "_groupInvalid" | "_peerInvalid" | "_groupChecked" | "_peerChecked" | "_groupFocusWithin" | "_peerFocusWithin" | "_peerPlaceholderShown" | "_placeholder" | "_placeholderShown" | "_fullScreen" | "_selection" | "_rtl" | "_ltr" | "_mediaDark" | "_mediaReduceMotion" | "_dark" | "_light")[];
//# sourceMappingURL=pseudos.d.ts.map