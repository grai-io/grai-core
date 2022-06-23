declare type SYMBOLS = " " | "D" | "∞" | "λ";
export interface IComponentWithPageModes {
    SSG: Set<string>;
    DSG: Set<string>;
    SSR: Set<string>;
    FN: Set<string>;
}
export interface IPageTreeLine {
    text: string;
    symbol: SYMBOLS;
}
export declare function generatePageTree(collections: IComponentWithPageModes, LIMIT?: number): Array<IPageTreeLine>;
export {};
