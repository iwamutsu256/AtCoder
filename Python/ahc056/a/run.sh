#!/bin/bash

# --- 1. スクリプトの安全設定 ---
# set -eu: エラーが発生したら(e) or 未定義変数を使ったら(u) 停止
set -eu

# --- 2. 引数のチェック ---
# $# は引数の数
if [ "$#" -ne 1 ]; then
    echo "エラー: 実行するPythonスクリプトの番号を引数で指定してください。"
    echo "例: bash run.sh 3  (main3.py を実行)"
    exit 1
fi

# --- 3. 変数の設定 ---
X=$1 # 引数からスクリプト番号 (例: 3) を取得
PYTHON_SCRIPT="main${X}.py"
OUTPUT_DIR="out${X}"
LOG_FILE="score_log_${X}.txt" # 実行ごとのログ
SUMMARY_FILE="summary_${X}.txt" # 最終的な統計サマリ

START_CASE=0
END_CASE=499
TOTAL_CASES=$(($END_CASE - $START_CASE + 1))

# --- 4. 実行前チェック ---
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "エラー: $PYTHON_SCRIPT が見つかりません。"
    exit 1
fi

# 出力ディレクトリを作成 (存在しなくてもエラーにしない -p)
mkdir -p "$OUTPUT_DIR"

# ログファイルを初期化 ( > $LOG_FILE だと set -u でエラーになることがある)
: > "$LOG_FILE"

echo "--- $PYTHON_SCRIPT の実行開始 (全 $TOTAL_CASES ケース) ---"
echo "入力: in/"
echo "出力: $OUTPUT_DIR/"
echo "ログ: $LOG_FILE"
echo "-------------------------------------------------"

# --- 5. 統計情報用変数の初期化 ---
# bc (計算用ライブラリ) 向けに初期化
total_score="0"
total_time="0.0"

# awkでの処理を簡単にするため、配列ではなく一時ファイルを使う
SCORE_TEMP_FILE=$(mktemp)
TIME_TEMP_FILE=$(mktemp)
# スクリプト終了時に一時ファイルを必ず削除する
trap 'rm -f $SCORE_TEMP_FILE $TIME_TEMP_FILE' EXIT


# --- 6. メインループ (0000.txt から 0499.txt) ---
for i in $(seq $START_CASE $END_CASE); do
    # iを4桁のゼロ埋め文字列にフォーマット (例: 5 -> 0005)
    i_padded=$(printf "%04d" "$i")
    INPUT_FILE="in/${i_padded}.txt"
    OUTPUT_FILE="${OUTPUT_DIR}/out${i_padded}.txt"
    
    # 一時的にstderr(スコアと時間)を格納するファイル
    STDERR_LOG="stderr_temp.log"

    # --- 実行 ---
    # /usr/bin/time -f "%e": 実行時間(秒)だけを stderr に出力
    # ( ... ) 2> $STDERR_LOG: 
    #   ()内の標準エラー出力(pythonのスコア + timeの実行時間)を $STDERR_LOG にリダイレクト
    ( /usr/bin/time -f "%e" python "$PYTHON_SCRIPT" < "$INPUT_FILE" > "$OUTPUT_FILE" ) 2> "$STDERR_LOG"

    # --- スコアのパース ---
    # 仮定: pythonがスコアを*1行目*に、timeが実行時間を*2行目*に出力する
    score=$(head -n 1 "$STDERR_LOG")
    
    # スコアが整数かチェック
    if ! [[ "$score" =~ ^[0-9]+$ ]]; then
        echo "ケース $i: スコアのパースに失敗 (score='$score')"
        score=0 # エラー時は0点として集計
    fi

    # --- 実行時間のパース ---
    exec_time=$(tail -n 1 "$STDERR_LOG")
    
    # --- ログファイルに記録 (tee -a: ファイルに追記しつつ標準出力にも出す) ---
    echo "Case $i_padded: Score = $score, Time = ${exec_time}s" | tee -a "$LOG_FILE"

    # --- 統計用 ---
    echo "$score" >> "$SCORE_TEMP_FILE"
    echo "$exec_time" >> "$TIME_TEMP_FILE"
    
    # bc を使って合計を加算
    total_score=$(echo "$total_score + $score" | bc)
    total_time=$(echo "$total_time + $exec_time" | bc)
    
    # ターミナルに進捗表示 ( \r で上書き)
    current_case_num=$(($i - $START_CASE + 1))
    printf "進捗: %d / %d (%.1f%%)\r" "$current_case_num" "$TOTAL_CASES" "$(echo "scale=1; 100 * $current_case_num / $TOTAL_CASES" | bc)"

done

rm "stderr_temp.log" # 一時ファイルを削除
echo # 改行
echo "--- 全 $TOTAL_CASES ケースの実行完了 ---"

# --- 7. 統計情報の計算と出力 ---
# awk を使って、一時ファイルから最小、最大、平均を計算
# sort -n: 数値として昇順ソート
# head -n 1: 最小値
# tail -n 1: 最大値

# スコア集計
min_score=$(sort -n "$SCORE_TEMP_FILE" | head -n 1)
max_score=$(sort -n "$SCORE_TEMP_FILE" | tail -n 1)
avg_score=$(echo "scale=2; $total_score / $TOTAL_CASES" | bc -l)

# 実行時間集計
min_time=$(sort -n "$TIME_TEMP_FILE" | head -n 1)
max_time=$(sort -n "$TIME_TEMP_FILE" | tail -n 1)
avg_time=$(echo "scale=3; $total_time / $TOTAL_CASES" | bc -l)

# --- サマリの表示とファイルへの保存 ---
# tee を使って、標準出力と summary_X.txt の両方に出力
{
    echo "--- 統計サマリ ($PYTHON_SCRIPT) ---"
    echo "[スコア]"
    echo "  合計点: $total_score"
    echo "  最大点: $max_score"
    echo "  最小点: $min_score"
    echo "  平均点: $avg_score"
    echo ""
    echo "[実行時間]"
    echo "  最大時間: ${max_time}s"
    echo "  最小時間: ${min_time}s"
    echo "  平均時間: ${avg_time}s"
    echo "-----------------------------------"
} | tee "$SUMMARY_FILE"

echo "サマリは $SUMMARY_FILE にも保存されました。"