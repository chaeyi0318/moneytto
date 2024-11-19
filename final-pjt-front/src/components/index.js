//index.js
/**
 *
 * @param {number} num
 * @param {number} length
 */
const pad = (num, length) => {
  return ('0000' + num).slice(-length)
}
const MILLIS = {
  day: 1 * 24 * 60 * 60 * 1000,
  week: 7 * 1 * 24 * 60 * 60 * 1000
}
/**
 *
 * @param {LocalDate} date
 * @param {number} delta
 * @param {string} unit
 */
const shiftDate = (date, delta, unit) => {
  const millis = delta * MILLIS[unit]
  const curMillis = date.value.getTime()
  return new LocalDate(new Date(curMillis + millis))
}
export class LocalDate {
  /**
   * @type {Date} date instance
   */
  value
  /**
   *
   * @param {Date} value
   */
  constructor(value) {
    this.value = value
  }
  get year() {
    return pad(this.value.getFullYear(), 4) //It is number
  }
  get month() {
    return pad(this.value.getMonth() + 1, 2) //number
  }
  get date() {
    return pad(this.value.getDate(), 2) //number
  }
  get ymdText() {
    const { year, month, date } = this
    return `${year}-${month}-${date}`
  }
  get weekOffset() {
    return this.value.getDay()
  }
  /**
   *
   * @param {number} delta
   * @param {string} unit  - 'day', 'week', ..
   */
  minus(delta, unit) {
    return shiftDate(this, -1 * delta, unit)
  }
  plus(delta, unit) {
    return shiftDate(this, delta, unit)
  }
  /**
   *
   * @param {LocalDate} date
   */
  equals(other) {
    return (
      other && other.year === this.year && other.month === this.month && other.date === this.date
    )
  }
}

/**
 *
 * @param {Number} year
 * @param {Number} month 1 ~ 12(not monthIndex)
 * @param {*} date 1 ~ 28, 30, 31
 * @returns
 */
LocalDate.fromYmd = (year, month, date) => {
  const value = new Date(year, month - 1, date)
  return new LocalDate(value)
}