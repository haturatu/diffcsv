#!/usr/bin/python

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    plt.figure(figsize=(12, 6))

    # ファイルごとにプロットしたいカラムを選択
    for i, df in enumerate(file_list):
        col = st.selectbox(f'ファイル{i+1}のカラムを選択してください', [col for col in df.columns if col != date_column], key=f'col_select_{i}')
        # データフレームごとにプロット
        plt.plot(df[date_column], df[col], label=f'{col} (File {i+1})')

    plt.xlabel(date_column)
    plt.ylabel('Value')
    plt.title('CSV to FRED')
    plt.legend()

    st.pyplot(plt.gcf())
else:
    st.write("CSVファイルをアップロードしてください。")

