// component/calendar/Calendar.js

import { LocalDate } from './LocalDate';
import { Week } from './Week';

export class Calendar {
  constructor(weeks) {
    this.weeks = weeks;
  }

  get firstWeek() {
    return this.weeks[0];
  }

  get lastWeek() {
    return this.weeks[this.weeks.length - 1];
  }

  get yearText() {
    return this.firstWeek.dayAt(0).year;
  }

  get monthText() {
    return this.firstWeek.dayAt(6).month;
  }

  getWeeks() {
    return this.weeks;
  }

  prevMonth() {
    const anyDayPrevMonth = this.firstWeek.prev().dayAt(0);
    const year = parseInt(anyDayPrevMonth.year);
    const month = parseInt(anyDayPrevMonth.month);
    return Calendar.fromYm(year, month);
  }

  nextMonth() {
    const anyDayNextMonth = this.lastWeek.next().dayAt(0);
    const year = parseInt(anyDayNextMonth.year);
    const month = parseInt(anyDayNextMonth.month);
    return Calendar.fromYm(year, month);
  }

  containsDate(date) {
    return date.month === this.monthText;
  }

  isToday(date) {
    const today = new LocalDate(new Date());
    return today.equals(date);
  }

  static fromYm(year, month) {
    const leadingDate = LocalDate.fromYmd(year, month, 1);
    const leadingWeek = Week.fromLocalDate(leadingDate);

    const weeksArray = [];
    let currentWeek = leadingWeek;

    while (weeksArray.length < 6) { // 최대 주 수는 보통 한 달에 최대 여섯 주
      weeksArray.push(currentWeek);
      currentWeek = currentWeek.next();
    }
    
    return new Calendar(weeksArray);
  }
}
