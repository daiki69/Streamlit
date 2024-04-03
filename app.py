# 必要なライブラリをダウンロード
import streamlit as st
import spacy
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

# spaCyで日本語テキストを処理するためのモデルをロード
nlp = spacy.load("ja_core_news_sm")

# 品詞情報を日本語に変換するための辞書
pos_dict = {
    'ADJ': '形容詞',
    'ADP': '助詞',
    'ADV': '副詞',
    'AUX': '助動詞',
    'CCONJ': '接続詞',
    'DET': '限定詞',
    'INTJ': '間投詞',
    'NOUN': '名詞',
    'NUM': '数詞',
    'PART': '助詞',
    'PRON': '代名詞',
    'PROPN': '固有名詞',
    'PUNCT': '句読点',
    'SCONJ': '補助接続詞',
    'SYM': '記号',
    'VERB': '動詞',
    'X': 'その他',
}

# テキストからキーワードを抽出する関数
def extract_keywords(text):
    doc = nlp(text)
    keywords = [(token.text, token.pos_) for token in doc if not token.is_stop and token.is_alpha]
    return keywords

# テキストデータからTF-IDFを計算する関数
def calculate_tfidf(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names

# ワードクラウドを生成する関数
def generate_wordcloud(text):
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/msgothic.ttc", width=1600, height=800, background_color='white', colormap='viridis').generate(text)
    return wordcloud

def main():
    st.title("キーフレーズ抽出アプリ")

    # テキスト入力
    text = st.text_area("テキストを入力してください", height=200)

    # スライダーで閾値を調整
    threshold = st.slider("フレーズごとの重要度-閾値", min_value=0.0, max_value=0.5, value=0.1, step=0.01)
    freq_threshold = st.slider("出現頻度-閾値", min_value=1, max_value=10, value=3, step=1)

    if st.button("キーフレーズ抽出"):
        # キーフレーズの抽出
        keywords = extract_keywords(text)
        processed_text = " ".join([keyword[0] for keyword in keywords])

        # TF-IDFを計算
        tfidf_matrix, feature_names = calculate_tfidf([processed_text])

        # フレーズごとの重要度を取得
        keyword_list = []
        importance_list = []
        for col in tfidf_matrix.nonzero()[1]:
            if tfidf_matrix[0, col] >= threshold:
                keyword_list.append(feature_names[col])
                importance_list.append(tfidf_matrix[0, col])

        # 単語の出現頻度を取得
        word_freq = Counter([keyword[0] for keyword in keywords])
        word_freq_list = [word_freq[word] for word in keyword_list]

        # 棒グラフで表示
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        ax1.barh(keyword_list, importance_list)
        ax1.invert_yaxis()
        ax1.set_xlabel('重要度')
        ax1.set_title('キーフレーズの重要度')
        st.pyplot(fig1)

        # 棒グラフで表示
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        ax2.barh(keyword_list, word_freq_list)
        ax2.invert_yaxis()
        ax2.set_xlabel('出現頻度')
        ax2.set_title('単語の出現頻度')
        st.pyplot(fig2)

        # Word Cloudで表示
        wordcloud = generate_wordcloud(processed_text)
        st.image(wordcloud.to_array(), use_column_width=True)

        # 品詞情報を含むデータフレームを作成
        df_pos = pd.DataFrame(keywords, columns=['単語', '品詞'])
        df_pos['品詞(JP)'] = df_pos['品詞'].map(pos_dict)

        data = {'単語': keyword_list, '品詞(EN)': [next((pos for word, pos in keywords if word == keyword), None) for keyword in keyword_list], '品詞(JP)': [pos_dict.get(pos, 'その他') for pos in [next((pos for word, pos in keywords if word == keyword), None) for keyword in keyword_list]], '出現頻度': word_freq_list, '重要度（TF-IDF）': importance_list}
        df_tfidf = pd.DataFrame(data)

        st.write("単語・品詞(EN)・品詞(JP)・出現頻度・重要度(TF-IDF):")
        st.write(df_tfidf)

if __name__ == "__main__":
    main()