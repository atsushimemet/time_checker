function transferDataToRawRawSheet() {
  const sourceSpreadsheet = SpreadsheetApp.openById(SOURCE_SPREADSHEET_ID);
  const targetSpreadsheet = SpreadsheetApp.openById(TARGET_SPREADSHEET_ID);
  const sourceSheet = sourceSpreadsheet.getSheetByName(SOURCE_SHEET_NAME_2);
  const targetSheet = targetSpreadsheet.getSheetByName(TARGET_SHEET_NAME_RAW_RAW);
  const sourceData = sourceSheet.getDataRange().getValues();
  // 新しい日付と曜日の列を追加
  const targetDate = new Date(); // または特定の日付を設定
  targetDate.setDate(targetDate.getDate() - DAY_BEFORE);
  const formattedDate = Utilities.formatDate(targetDate, Session.getScriptTimeZone(), 'yyyy/MM/dd');
  const formattedWeekday = getWeekday(targetDate);
  const lastColumn = targetSheet.getLastColumn();
  targetSheet.getRange(1, lastColumn + 1).setValue(formattedDate);
  targetSheet.getRange(2, lastColumn + 1).setValue(formattedWeekday);
  // データのコピー
  sourceData.forEach((row, index) => {
    targetSheet.getRange(index + 3, lastColumn + 1).setValue(row[1]); // 3行目から始める（1行目は日付、2行目は曜日）
  });
  // 最後の行に「24」を挿入。このタイミングでは合計が24時間であることが保証されている。
  const lastRow = targetSheet.getLastRow();
  targetSheet.getRange(lastRow, lastColumn + 1).setValue(24);
}