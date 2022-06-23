import * as CSS from "csstype";
import { Config } from "../utils/prop-config";
import { Token } from "../utils";
export declare const scroll: Config;
export interface ScrollProps {
    scrollBehavior?: Token<CSS.Property.ScrollBehavior>;
    scrollSnapAlign?: Token<CSS.Property.ScrollSnapAlign>;
    scrollSnapStop?: Token<CSS.Property.ScrollSnapStop>;
    scrollSnapType?: Token<CSS.Property.ScrollSnapType>;
    scrollMargin?: Token<CSS.Property.ScrollMargin | number, "space">;
    scrollMarginTop?: Token<CSS.Property.ScrollMarginTop | number, "space">;
    scrollMarginBottom?: Token<CSS.Property.ScrollMarginBottom | number, "space">;
    scrollMarginLeft?: Token<CSS.Property.ScrollMarginLeft | number, "space">;
    scrollMarginRight?: Token<CSS.Property.ScrollMarginRight | number, "space">;
    scrollMarginX?: Token<CSS.Property.ScrollMargin | number, "space">;
    scrollMarginY?: Token<CSS.Property.ScrollMargin | number, "space">;
    scrollPadding?: Token<CSS.Property.ScrollPadding | number, "space">;
    scrollPaddingTop?: Token<CSS.Property.ScrollPaddingTop | number, "space">;
    scrollPaddingBottom?: Token<CSS.Property.ScrollPaddingBottom | number, "space">;
    scrollPaddingLeft?: Token<CSS.Property.ScrollPaddingLeft | number, "space">;
    scrollPaddingRight?: Token<CSS.Property.ScrollPaddingRight | number, "space">;
    scrollPaddingX?: Token<CSS.Property.ScrollPadding | number, "space">;
    scrollPaddingY?: Token<CSS.Property.ScrollPadding | number, "space">;
}
//# sourceMappingURL=scroll.d.ts.map