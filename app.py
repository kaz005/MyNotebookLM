import streamlit as st
import tempfile
import os
import yaml
from extractor import extract_article_text
from summarizer import summarize_article
from tts import synthesize_speech

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    st.title("AI要約・解説＆音声化ツール")
    config = load_config()

    st.write("### 入力方法を選択してください")
    input_mode = st.radio("入力タイプ", ("URL", "画像アップロード", "テキスト入力"))

    input_str = None
    if input_mode == "URL":
        url = st.text_input("Web記事のURLを入力")
        if url:
            input_str = url
    elif input_mode == "画像アップロード":
        uploaded_file = st.file_uploader("画像ファイルをアップロード", type=["png", "jpg", "jpeg", "bmp", "gif"])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                input_str = tmp_file.name
    else:
        text = st.text_area("テキストを直接入力")
        if text:
            input_str = text

    if input_str and st.button("AIで要約・音声化"):
        with st.spinner("本文・テキスト抽出中..."):
            article_text = extract_article_text(input_str)
        st.subheader("抽出テキスト")
        st.write(article_text[:1000] + ("..." if len(article_text) > 1000 else ""))

        with st.spinner("要約・解説生成中..."):
            summary = summarize_article(article_text, config)
        st.subheader("要約・解説")
        st.write(summary)

        with st.spinner("音声合成中..."):
            audio_path = synthesize_speech(summary, config)
        st.subheader("音声再生")
        audio_bytes = open(audio_path, 'rb').read()
        st.audio(audio_bytes, format='audio/mp3')
        # 一時ファイル削除
        if input_mode == "画像アップロード" and input_str:
            os.remove(input_str)
        os.remove(audio_path)

if __name__ == "__main__":
    main() 