function getWeekday(date) {
  const weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
  return weekdays[date.getDay()];
}
