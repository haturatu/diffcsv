#!/usr/bin/python

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 日本語フォントの設定
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

# Streamlitアプリケーションのタイトル設定
st.title('CSVファイル比較チャート')

# アップロードボックスの作成
uploaded_files = st.file_uploader("ここにCSVファイルをドラッグ＆ドロップ", type=['csv'], accept_multiple_files=True)

if uploaded_files:
    # ファイルの最大数を10に制限
    if len(uploaded_files) > 10:
        st.error("最大10個のファイルをアップロードしてください。")
        st.stop()

    # アップロードされたファイルをリストとして処理
    file_list = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        file_list.append(df)
        st.write(f"アップロードされたファイルのカラム名: {df.columns.tolist()}")

    date_column = 'DATE'  # 日付カラムのデフォルト値

    # 各DataFrameに対して日付カラムの存在を確認
    for df in file_list:
        if date_column not in df.columns:  # 日付カラムが存在しない場合、エラーメッセージを表示
            st.error(f"各CSVファイルには'{date_column}'という名前の日付カラムが必要です。カラム名: {df.columns.tolist()}")
            st.stop()
        df[date_column] = pd.to_datetime(df[date_column])

    # プロットの作成
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    for i, df in enumerate(file_list):
        # ファイルごとに縦軸の位置を選択するためのセレクトボックスを作成
        axis_position = st.selectbox(f'ファイル{i+1}の縦軸の位置を選択してください', ["左", "右"], index=0, key=f'axis_position_{i}')

        # ファイルごとにプロットしたいカラムを選択
        col = st.selectbox(f'ファイル{i+1}のカラムを選択してください', [col for col in df.columns if col != date_column], key=f'col_select_{i}')

        # 凡例名を入力するためのテキストボックスを作成
        legend_name = st.text_input(f'ファイル{i+1}の凡例名を入力してください（デフォルトはカラム名: {col}）', col, key=f'legend_input_{i}')

        # 縦軸の位置に応じてデータフレームをプロット
        if axis_position == "左":
            ax1.plot(df[date_column], df[col], label=legend_name, color=f'C{i}')
        else:
            ax2.plot(df[date_column], df[col], label=legend_name, color=f'C{i}', linestyle='--')

    ax1.set_xlabel(date_column)
    ax1.set_ylabel('')
    ax2.set_ylabel('')

    # 凡例の設定（左軸の凡例を右側に、右軸の凡例を左側に）
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles2, labels2, loc='upper left')
    ax2.legend(handles1, labels1, loc='upper right')

    plt.title('CSV to plot')
    st.pyplot(fig)
else:
    st.write("CSVファイルをアップロードしてください。")

