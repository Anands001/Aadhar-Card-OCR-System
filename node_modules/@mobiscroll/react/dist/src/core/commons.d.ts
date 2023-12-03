import { MbscPopupDisplay } from './components/popup/popup.types.public';
import { Observable } from './util/observable';
export interface MbscCalendarSystem {
    getDate?: (y: number, m: number, d: number, h?: number, i?: number, s?: number, u?: number) => Date;
    getDay?: (d: Date) => number;
    getMaxDayOfMonth?: (y: number, m: number) => number;
    getMonth?: (d: Date) => number;
    getWeekNumber?: (d: Date) => number;
    getYear?: (d: Date) => number;
}
export interface MbscOptions {
    calendarSystem?: MbscCalendarSystem;
    display?: MbscPopupDisplay;
    locale?: any;
    rtl?: boolean;
    theme?: string;
    themeVariant?: string;
}
/** @hidden */
export declare const options: MbscOptions;
/** @hidden */
export declare const util: any;
/** @hidden */
export declare const themes: {
    [key: string]: any;
};
/** @hidden */
export declare const autoDetect: {
    theme?: string;
};
/** @hidden */
export declare const globalChanges: Observable<MbscOptions>;
/** @hidden */
export declare function getAutoTheme(): string;
export declare function setOptions(local: Partial<MbscOptions> & {
    [other: string]: any;
}): void;
/**
 * Creates a custom theme definition object. It inherits the defaults from the specified base theme.
 * @param name Name of the custom theme.
 * @param baseTheme Name of the base theme (ios, material or windows).
 * @param auto Allow to set it as auto theme, if the component has theme: 'auto' set. True, if not set.
 */
export declare function createCustomTheme(name: string, baseTheme: string, auto?: boolean): void;
export declare const platform: {
    majorVersion: number;
    minorVersion: number;
    name: string;
};
