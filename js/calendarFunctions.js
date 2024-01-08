function extractAndCheckTotalTime() {
  const spreadsheet = SpreadsheetApp.openById(SOURCE_SPREADSHEET_ID);
  const sheet = spreadsheet.getSheetByName(SOURCE_SHEET_NAME_1);
  // Clear existing content in sheet
  sheet.clear();
  // 昨日の日付を取得
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - DAY_BEFORE);
  // カレンダー情報ごとに予定を取得してスプレッドシートに出力
  for (const calendarInfo of CALENDAR_INFO) {
    const calendarId = calendarInfo.id;
    const calendarName = calendarInfo.name;
    // カレンダーから昨日の予定を取得
    const calendar = CalendarApp.getCalendarById(calendarId);
    const events = calendar.getEventsForDay(yesterday);
    // [0-9].[0-9][0-9]のパターンを持つ予定を抽出してスプレッドシートに出力
    for (const event of events) {
      const title = event.getTitle();
      const startTime = event.getStartTime();
      const endTime = event.getEndTime();
      // [0-9].[0-9][0-9]のパターンを検索
      const regex = /[0-9]+\.[0-9][0-9]/;
      if (regex.test(title)) {
        // 時間計算
        const durationMinutes = (endTime - startTime) / (1000 * 60); // 分単位に変換
        const durationHours = durationMinutes / 60; // 時間単位に変換
        // スプレッドシートに出力
        sheet.appendRow([title, calendarName, durationHours]);
      }
    }
  }
  // 各カレンダーから取得した予定を合計して、24時間かどうかを確認
  let totalDurationAcrossCalendars = 0;
  for (const calendarInfo of CALENDAR_INFO) {
    const calendarName = calendarInfo.name;
    const dataRange = sheet.getDataRange();
    const values = dataRange.getValues();
    for (const row of values) {
      if (row[1] === calendarName) {
        totalDurationAcrossCalendars += row[2];
      }
    }
  }
  // 合計時間が24時間でない場合はエラーを送出
  if (Math.abs(totalDurationAcrossCalendars - 24) > 0.01) {
    Logger.log('合計が' + totalDurationAcrossCalendars + '時間です');    
    throw new Error('カレンダー全体の合計時間が24時間ではありません。');
  }
  Logger.log('昨日の[0-9].[0-9][0-9]のパターンを持つ予定がスプレッドシートに出力されました');
}

function calculateCategoryTotals() {
  const CATEGORIES = ['Sleep', 'MorningRoutine', 'Personal', 'RegularRevenue', 'House', 'Vook&NewBusiness', 'Friends', 'Training', 'Move', 'Study'];
  const spreadsheet = SpreadsheetApp.openById(SOURCE_SPREADSHEET_ID);
  const sheet1 = spreadsheet.getSheetByName(SOURCE_SHEET_NAME_1);
  const sheet2 = spreadsheet.getSheetByName(SOURCE_SHEET_NAME_2) || spreadsheet.insertSheet(SOURCE_SHEET_NAME_2);
  // Clear existing content in Sheet2
  sheet2.clear();
  const sheet1Data = sheet1.getDataRange().getValues();
  // Creating an object to store the total durations of each category
  let categoryDurations = {};
  CATEGORIES.forEach(category => categoryDurations[category] = 0);
  // Summing the durations from Sheet1
  sheet1Data.forEach(row => {
    const category = row[1];
    const duration = parseFloat(row[2]);
    if (categoryDurations.hasOwnProperty(category)) {
      categoryDurations[category] += duration;
    }
  });
  // Writing the totals to Sheet2
  CATEGORIES.forEach(category => {
    sheet2.appendRow([category, categoryDurations[category]]);
  });
  Logger.log('カテゴリごとの合計時間がシート2に出力されました');
}
