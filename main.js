function main() {
  try {
    extractAndCheckTotalTime();
    Logger.log('extractAndCheckTotalTime関数が正常に完了しました。');
    calculateCategoryTotals();
    Logger.log('calculateCategoryTotals関数が正常に完了しました。');
    transferDataToRawRawSheet();
    Logger.log('raw_rawシートへのデータ転送が完了しました。');
  } catch (error) {
    Logger.log('エラーが発生しました: ' + error.message);
  }
}