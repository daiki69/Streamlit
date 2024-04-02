import streamlit as st
import csv
import datetime
import os
import base64

def generate_csv(start_time, end_time, interval_count):
    try:
        day_interval = (end_time - start_time) / int(interval_count)

        time_list = [start_time + i * day_interval for i in range(int(interval_count) + 1)]

        # CSVファイルを生成する
        fieldnames = ['Time']
        rows = []
        for time in time_list:
            time = datetime.datetime.combine(time, datetime.time.min)
            rows.append({'Time': time.strftime('%Y/%m/%d')})

        # ダウンロード用の一時ファイルを作成する
        temp_file_path = os.path.join(os.getcwd(), '4DCreate.csv')
        with open(temp_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        # ダウンロードリンクを表示する
        st.markdown(get_download_link(temp_file_path), unsafe_allow_html=True)
        
        st.success("CSVファイルが正常に生成されました！ダウンロードをクリック！")
        
    except ValueError:
        st.error("無効な入力です。正しい値を入力してください。")
        

        

def get_download_link(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        file_name = os.path.basename(file_path)
        encoded_content = base64.b64encode(file_content).decode()
        href = f'<a href="data:file/csv;base64,{encoded_content}" download="{file_name}">ダウンロード</a>'
    return href

# カレンダーの表示を日本語に設定する
def set_japanese_locale():
    return "%Y-%m-%d"

# Streamlitアプリを作成する
st.set_page_config(page_title="Fuzor4D作成支援ツール")
st.title("Fuzor4D作成支援ツール")

# 画像を表示する
image_path = "FuzorLogo.png"  # 画像のパスを指定
st.image(image_path, caption="4DFuzor", use_column_width=True)

# 開始日時の入力フィールドを作成する
start_time = st.date_input("開始日時", value=datetime.date.today(), key='start')

# 終了日時の入力フィールドを作成する
end_time = st.date_input("終了日時", value=datetime.date.today(), key='end')

# 分割数の入力フィールドを作成する
interval_count = st.number_input("分割数", min_value=1, step=1)

# 説明文を表示する
st.markdown("""   \n
            工程の開始日・終了日を選択し、分割数を指定し、CSV生成ボタンを押してください。   \n
             \n
            最適化された日付タスクのリストを出力します。  \n
            出力されたCSVはExcelで開くことが出来ます。
            """)

# CSVファイルを生成するボタンを作成する
if st.button("CSV生成"):
    generate_csv(start_time, end_time, interval_count)


st.write("\n取扱説明マニュアルは下記ボタンをクリックしてください。")
st.link_button("マニュアルページへ", "https://daikino.notion.site/4D-csv-4D-270f83d85b08405aa79d0323dd4e5bec?pvs=4")
