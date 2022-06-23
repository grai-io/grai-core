import { Union } from "../utils";
export declare type SemanticValue<Conditions extends string, Token extends string = string> = Union<Token> | Partial<Record<"default" | Conditions, Union<Token>>>;
export declare type PlainToken = {
    isSemantic: false;
    value: string | number;
};
export declare type SemanticToken = {
    isSemantic: true;
    value: string | number | SemanticValue<string>;
};
export declare type FlatToken = PlainToken | SemanticToken;
export declare type FlatTokens = Record<string, FlatToken>;
export declare type FlattenTokensParam = {
    tokens?: object;
    semanticTokens?: object;
};
export declare function flattenTokens<T extends FlattenTokensParam>({ tokens, semanticTokens, }: T): FlatTokens;
//# sourceMappingURL=flatten-tokens.d.ts.map