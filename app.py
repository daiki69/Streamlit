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

nlp = spacy.load("ja_core_news_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return keywords

def calculate_tfidf(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names

def generate_wordcloud(text):
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/msgothic.ttc", width=1600, height=800, background_color='white', colormap='viridis').generate(text)
    return wordcloud

def main():
    st.title("キーフレーズ抽出アプリ")

    # テキスト入力
    text = st.text_area("テキストを入力してください", height=200)

    threshold = st.slider("閾値", min_value=0.0, max_value=0.5, value=0.1, step=0.01)

    if st.button("キーフレーズ抽出"):
        # キーフレーズの抽出
        keywords = extract_keywords(text)
        processed_text = " ".join(keywords)

        # TF-IDFを計算
        tfidf_matrix, feature_names = calculate_tfidf([processed_text])

        # フレーズごとの重要度を取得
        keyword_list = []
        importance_list = []
        for col in tfidf_matrix.nonzero()[1]:
            if tfidf_matrix[0, col] >= threshold:
                keyword_list.append(feature_names[col])
                importance_list.append(tfidf_matrix[0, col])

        # 棒グラフで表示
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.barh(keyword_list, importance_list)
        ax1.invert_yaxis()  # 重要度が高いキーフレーズが上に表示されるようにする
        ax1.set_xlabel('重要度')
        ax1.set_title('キーフレーズの重要度')
        st.pyplot(fig1)

        # ヒストグラムで表示
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        ax2.hist(importance_list, bins=20, color='skyblue', edgecolor='black')
        ax2.set_xlabel('重要度')
        ax2.set_ylabel('頻度')
        ax2.set_title('キーフレーズの重要度分布')
        st.pyplot(fig2)

        # 単語の出現頻度を取得
        word_freq = Counter(keywords)
        word_freq_list = [word_freq[keyword] for keyword in keyword_list]

        # Word Cloudで表示
        wordcloud = generate_wordcloud(processed_text)
        st.image(wordcloud.to_array(), use_column_width=True)

        # 単語の出現頻度および重要度を含むデータフレームを作成
        word_freq = Counter(keywords)
        data = {'単語': list(word_freq.keys()), '出現頻度': list(word_freq.values()), '重要度': [tfidf_matrix[0, feature_names.tolist().index(word)] if word in feature_names.tolist() else 0.0 for word in word_freq.keys()]}
        df = pd.DataFrame(data)

        # CSVファイルに出力
        st.write("CSVファイルに出力:")
        st.write(df)
        csv = df.to_csv(index=True)

if __name__ == "__main__":
    main()