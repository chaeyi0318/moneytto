// component/calendar/Week.js

export class Week {
  constructor(leadingDate) {
    this.date = leadingDate;
  }

  dayAt(weekOffset) {
    return this.date.plus(weekOffset, 'day');
  }

  days() {
    const daysArray = [];
    for (let i = 0; i < 7; i++) {
      daysArray.push(this.dayAt(i));
    }
    return daysArray;
  }

  prev() {
    return new Week(this.date.minus(7, 'day'));
  }

  next() {
    return new Week(this.date.plus(7, 'day'));
  }

  static fromLocalDate(date) {
    const offset = date.weekOffset;
    const sunday = date.minus(offset, 'day');
    return new Week(sunday);
  }
}
