# #!/bin/bash

# # 検索するディレクトリ（現在のディレクトリをデフォルトとする）
# SEARCH_DIR=${1:-.}

# # 検出するシークレットのパターン
# # メールアドレスと特定のID形式のパターンを正規表現で定義
# PATTERNS=(
#   '[a-zA-Z0-9._%+-]+@group\.calendar\.google\.com' # メールアドレス
#   '[0-9a-zA-Z_-]{22,}'                             # 特定のID形式
# )

# # パターンに一致する行を検索
# for pattern in "${PATTERNS[@]}"; do
#   echo "Searching for pattern: $pattern"
#   grep -rl $SEARCH_DIR -e $pattern
# done
