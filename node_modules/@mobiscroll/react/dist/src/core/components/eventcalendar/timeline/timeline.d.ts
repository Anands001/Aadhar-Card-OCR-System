import { MbscResource } from '../../../shared/calendar-view/calendar-view.types';
import { MbscSlotData } from '../eventcalendar.types';
import { STBase } from '../shared/schedule-timeline-base';
import { IDayData, ISTOptions, ISTState } from '../shared/schedule-timeline-base.types';
export interface ITimelineOptions extends ISTOptions {
    dayTemplate?: any;
    type: 'week' | 'day' | 'month' | 'year';
    renderSlot?(args: MbscSlotData): any;
}
export interface ITimelineState extends ISTState {
    dayIndex: number;
}
export interface IConnectionData {
    color?: string;
    cssClass?: string;
    fill?: string;
    id: string;
    pathD: string;
    startDate: Date;
    endDate: Date;
}
/** @hidden */
export declare class TimelineBase extends STBase<ITimelineOptions, ITimelineState> {
    _isTimeline: boolean;
    _connections?: IConnectionData[];
    _stickyDay: IDayData;
    protected _stickyHeader: HTMLElement | null;
    protected _stickyDate: HTMLElement | null;
    protected _stickyMonth: HTMLElement | null;
    protected _stickyWeek: HTMLElement | null;
    private _scrollDebounce;
    _onScroll: () => void;
    _onParentClick(domEvent: any, resource: MbscResource): void;
    _setStickyHeader: (el: any) => void;
    _setStickyFooter: (el: any) => void;
    _setStickyDay: (el: any) => void;
    _setStickyMonth: (el: any) => void;
    _setStickyWeek: (el: any) => void;
    _setCont: (el: any) => void;
    _setResCont: (el: any) => void;
    _setSidebarCont: (el: any) => void;
    _setGridCont: (el: any) => void;
    _setHeaderCont: (el: any) => void;
    _setFooterCont: (el: any) => void;
    _setCursorTimeCont: (el: any) => void;
    protected _render(s: ITimelineOptions, state: ITimelineState): void;
}
