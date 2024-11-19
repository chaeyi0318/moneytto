// component/calendar/LocalDate.js

export class LocalDate {
  constructor(value) {
    this.value = value;
  }

  get year() {
    return this.value.getFullYear().toString().padStart(4, '0');
  }

  get month() {
    return (this.value.getMonth() + 1).toString().padStart(2, '0');
  }

  get date() {
    return this.value.getDate().toString().padStart(2, '0');
  }

  get ymdText() {
    return `${this.year}-${this.month}-${this.date}`;
  }

  get weekOffset() {
    return this.value.getDay();
  }

  minus(delta, unit) {
    const millis = delta * (unit === 'day' ? 86400000 : 604800000);
    const newDate = new Date(this.value.getTime() - millis);
    return new LocalDate(newDate);
  }

  plus(delta, unit) {
    const millis = delta * (unit === 'day' ? 86400000 : 604800000);
    const newDate = new Date(this.value.getTime() + millis);
    return new LocalDate(newDate);
  }

  equals(other) {
    return other.year === this.year && other.month === this.month && other.date === this.date;
  }

  static fromYmd(year, month, date) {
    return new LocalDate(new Date(year, month - 1, date));
  }
}
