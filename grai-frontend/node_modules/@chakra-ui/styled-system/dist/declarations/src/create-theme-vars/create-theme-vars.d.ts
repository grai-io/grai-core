import { Dict } from "@chakra-ui/utils";
import { FlatTokens } from "./flatten-tokens";
export interface CreateThemeVarsOptions {
    cssVarPrefix?: string;
}
export interface ThemeVars {
    cssVars: Dict;
    cssMap: Dict;
}
export declare function createThemeVars(flatTokens: FlatTokens, options: CreateThemeVarsOptions): {
    cssVars: {};
    cssMap: {};
};
//# sourceMappingURL=create-theme-vars.d.ts.map