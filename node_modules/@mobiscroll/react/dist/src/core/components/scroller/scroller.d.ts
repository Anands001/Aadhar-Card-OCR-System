import { MbscPopupDisplay } from '../../components/popup/popup.types.public';
import { PickerBase } from '../../shared/picker/picker';
import { IActiveChangeArgs, IWheelIndexChangeArgs } from '../../shared/wheel/wheel';
import { MbscScrollerOptions, MbscScrollerState, MbscScrollerWheel } from './scroller.types';
/**
 * Returns the closest valid value on a wheel.
 * @hidden
 * @param wheel The wheel object.
 * @param val The current value.
 * @param direction Direction of the wheel movement.
 * @param disabled Disabled values on the wheel.
 */
export declare function getValid(wheel: MbscScrollerWheel, val: any, disabled?: Map<any, boolean>, direction?: number): any;
/** @hidden */
export declare class ScrollerBase extends PickerBase<MbscScrollerOptions, MbscScrollerState, any, any[]> {
    /** @hidden */
    static defaults: MbscScrollerOptions;
    protected static _name: string;
    /** @hidden */
    _circular?: boolean | boolean[];
    /** @hidden */
    _disabled?: Array<Map<any, boolean>>;
    /** @hidden */
    _displayStyle?: MbscPopupDisplay;
    /** @hidden */
    _indexes: number[];
    /** @hidden */
    _activeIndexes: number[];
    /** @hidden */
    _lineStyle?: any;
    /** @hidden */
    _overlayStyle?: any;
    /** @hidden */
    _rows: number;
    /** @hidden */
    _scroll3d: boolean;
    /** @hidden */
    _wheels: MbscScrollerWheel[][];
    private _batches;
    /**
     * Stores the last index that was set when selecting a value
     * Check out the _setIndexes method for more explanations.
     */
    private _lastIndexes;
    private _shouldSetIndex?;
    private _indexFromValue?;
    private _wheelMap;
    _onSet: () => void;
    /**
     * Triggered when the active item is changed via keyboard navigation.
     * When the selectOnScroll is true the onWheelIndexChange is triggered instead,
     * because selection also happens.
     */
    _onActiveChange: ({ wheel, index }: IActiveChangeArgs) => void;
    _onWheelIndexChange: (args: IWheelIndexChangeArgs) => void;
    _initWheels(): void;
    _shouldValidate(s: MbscScrollerOptions, prevS: MbscScrollerOptions): boolean;
    _valueEquals(v1: any, v2: any): boolean;
    protected _render(s: MbscScrollerOptions, state: MbscScrollerState): void;
    protected _writeValue(elm: HTMLInputElement, text: string, value: any): boolean;
    protected _copy(value: any[]): any[];
    protected _format(value: any[]): string;
    protected _get(value: any[]): any;
    protected _parse(valueStr: string): any[];
    /**
     * Does the validation
     * @param index Index of the wheel
     * @param direction Direction the wheel was moved
     */
    protected _validate(index?: number, direction?: number): void;
    protected _onOpen(): void;
    protected _onParse(): void;
    private _initWheel;
    /** Indexes must be set in two occasions:
     * 1. When the picker is opened
     * 2. When the wheels are changed (ex. Select filtering)
     *
     * The new index can come from the value (when opening the scroller), or from the currently scrolled to item
     */
    private _setIndexes;
    /**
     * The newIndex is the index of the topmost visible item on the scroller, but the selected item can be under that.
     * So if the newIndex comes from the selected value, the newIndex can turn up greater than the topmost item's
     * index. So we need to constrain the newIndex in this case, otherwise at the end of the list, there will be an
     * empty space
     * @param newIndex
     * @param wheel
     */
    private _constrainIndex;
}
