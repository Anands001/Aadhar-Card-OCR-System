import { BaseComponent } from '../../base';
import { MbscSegmentedGroupOptions } from './segmented.types.public';
/** @hidden */
export declare class SegmentedGroupBase extends BaseComponent<MbscSegmentedGroupOptions, any> {
    static defaults: MbscSegmentedGroupOptions;
    protected static _name: string;
    _groupClass?: string;
    _groupOpt: any;
    _name: string;
    private _unlisten?;
    private _id;
    _onChange: (ev: any, val: any) => void;
    _change(value: any): void;
    protected _render(s: MbscSegmentedGroupOptions): void;
    protected _updated(): void;
    protected _destroy(): void;
    private _setupDrag;
    private _cleanupDrag;
}
