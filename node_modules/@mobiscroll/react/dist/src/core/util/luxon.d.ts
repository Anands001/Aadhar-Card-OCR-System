import { IDate, ITimezonePlugin } from './datetime';
export declare class LDate implements IDate {
    _mbsc: boolean;
    private dt;
    private zone;
    constructor(value?: string | number | Date | number[], timezone?: string);
    clone(): LDate;
    createDate(value: number | Date): IDate;
    /**
     * Converts a Date object to a string.
     */
    [Symbol.toPrimitive](hint: 'number'): number;
    [Symbol.toPrimitive](hint: 'default' | 'string'): string;
    toDateString(): any;
    toISOString(): any;
    toJSON(): any;
    valueOf(): any;
    getDate(): any;
    getDay(): number;
    getFullYear(): any;
    getHours(): any;
    getMilliseconds(): any;
    getMinutes(): any;
    getMonth(): number;
    getSeconds(): any;
    getTime(): any;
    getTimezoneOffset(): number;
    getUTCDate(): any;
    getUTCDay(): number;
    getUTCFullYear(): any;
    getUTCHours(): any;
    getUTCMilliseconds(): any;
    getUTCMinutes(): any;
    getUTCMonth(): number;
    getUTCSeconds(): any;
    setMilliseconds(millisecond: number): any;
    setSeconds(second: number, millisecond?: number): any;
    setMinutes(minute: number, second?: number, millisecond?: number): any;
    setHours(hour: number, minute?: number, second?: number, millisecond?: number): any;
    setDate(day: number): any;
    setMonth(month: number, day?: number): any;
    setFullYear(year: number, month?: number, day?: number): any;
    setTime(time: number): any;
    setTimezone(timezone: string): void;
    setUTCMilliseconds(ms: number): number;
    setUTCSeconds(sec: number, ms?: number): number;
    setUTCMinutes(min: number, sec?: number, ms?: number): number;
    setUTCHours(hours: number, min?: number, sec?: number, ms?: number): number;
    setUTCDate(date: number): number;
    setUTCMonth(month: number, date?: number): number;
    setUTCFullYear(year: number, month?: number, date?: number): number;
    toUTCString(): string;
    toTimeString(): string;
    toLocaleDateString(): string;
    toLocaleTimeString(): string;
    private setter;
}
export interface ILuxonTimezonePlugin extends ITimezonePlugin {
    luxon: any;
    version?: number;
}
/** @hidden */
export declare const luxonTimezone: ILuxonTimezonePlugin;
