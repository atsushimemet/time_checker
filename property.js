// 何日前の集計をするか
const DAY_BEFORE = PropertiesService.getScriptProperties().getProperty('DAY_BEFORE');
function getProperty(key) {
  return PropertiesService.getScriptProperties().getProperty(key);
}
const SOURCE_SPREADSHEET_ID = getProperty('SOURCE_SPREADSHEET_ID');
const SOURCE_SHEET_NAME_1 = getProperty('SOURCE_SHEET_NAME_1');
const SOURCE_SHEET_NAME_2 = getProperty('SOURCE_SHEET_NAME_2');
const TARGET_SPREADSHEET_ID = getProperty('TARGET_SPREADSHEET_ID');
const TARGET_SHEET_NAME_RAW_RAW = getProperty('TARGET_SHEET_NAME_RAW_RAW');
// カレンダー情報
const CALENDAR_INFO = [
  { id: getProperty('Personal_ID'), name: 'Personal' },
  { id: getProperty('Friends_ID'), name: 'Friends' },
  { id: getProperty('House_ID'), name: 'House' },
  { id: getProperty('MorningRoutine_ID'), name: 'MorningRoutine' },
  { id: getProperty('Move_ID'), name: 'Move' },
  { id: getProperty('RegularRevenue_ID'), name: 'RegularRevenue' },
  { id: getProperty('Study_ID'), name: 'Study' },
  { id: getProperty('Training_ID'), name: 'Training' },
  { id: getProperty('Vook&NewBusiness_ID'), name: 'Vook&NewBusiness' },
  { id: getProperty('Sleep_ID'), name: 'Sleep' },
];