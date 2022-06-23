import { MachineConfig } from "xstate";
import { IQueryRunningContext } from "./types";
export declare const queryStates: MachineConfig<IQueryRunningContext, any, any>;
export declare const queryRunningMachine: import("xstate").StateMachine<IQueryRunningContext, any, any, {
    value: any;
    context: IQueryRunningContext;
}, import("xstate").ActionObject<IQueryRunningContext, any>>;
