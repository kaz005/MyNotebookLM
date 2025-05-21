from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import tempfile
import os
import yaml
from extractor import extract_article_text
from summarizer import summarize_article
from tts import synthesize_speech

# --- ダーク/ライト両対応カスタムCSS ---
st.markdown('''
    <style>
    html, body, [class*="css"]  { color-scheme: light dark; }
    .main {background-color: var(--background-color, #f7f9fa);}
    .stButton>button {
        background-color: #005bac;
        color: #fff;
        font-weight: bold;
        border-radius: 6px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #003e7e;
        color: #fff;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: var(--input-bg, #fff);
        color: var(--input-fg, #222);
        border: 1.5px solid #005bac;
        border-radius: 6px;
    }
    .stTextInput>div>input:disabled, .stTextArea>div>textarea:disabled {
        background-color: #e0e0e0;
        color: #888;
    }
    .stRadio>div>label, .stRadio>div>div>label {
        font-weight: 600;
        color: var(--radio-fg, #222);
    }
    .stSidebar {background-color: var(--sidebar-bg, #e9eef2);}
    .stSubheader, .stMarkdown h3, .stMarkdown h1 {
        color: #005bac !important;
    }
    /* ダークモード対応 */
    @media (prefers-color-scheme: dark) {
        .main {background-color: #22272b;}
        .stSidebar {background-color: #1a1d21;}
        .stTextInput>div>input, .stTextArea>div>textarea {
            background-color: #2c313a;
            color: #fff;
            border: 1.5px solid #3399ff;
        }
        .stRadio>div>label, .stRadio>div>div>label {
            color: #fff;
        }
        .stButton>button {
            background-color: #3399ff;
            color: #fff;
        }
        .stButton>button:hover {
            background-color: #1976d2;
        }
        .stSubheader, .stMarkdown h3, .stMarkdown h1 {
            color: #3399ff !important;
        }
    }
    </style>
''', unsafe_allow_html=True)

# --- サイドバー ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
st.sidebar.title("MyNotebookLM")
st.sidebar.markdown("""
#### AI要約・解説＆音声化ツール
- Web記事・画像・テキストをAIで要約
- 日本語音声で再生・ダウンロード

*Powered by OpenAI, Gemini, gTTS*
""")
st.sidebar.info("ビジネス用途・社内ナレッジ共有にも最適です。\n\n[使い方ガイド](https://github.com/yourrepo) | [お問い合わせ](mailto:support@example.com)")


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    st.markdown("""
    <h1 style='color:#005bac;'>📝 MyNotebookLM <span style='font-size:0.6em;color:#888;'>(AI要約・音声化)</span></h1>
    <div style='font-size:1.1em;color:#333;margin-bottom:1em;'>
    ビジネス文書・記事・画像をAIで要約し、日本語音声で再生・保存できます。
    </div>
    """, unsafe_allow_html=True)
    config = load_config()

    st.markdown("---")
    st.write("### 入力方法を選択してください")
    input_mode = st.radio("入力タイプ", ("URL", "画像アップロード", "テキスト入力"))

    input_str = None
    if input_mode == "URL":
        url = st.text_input("Web記事のURLを入力", help="例: https://news.yahoo.co.jp/...")
        if url:
            input_str = url
    elif input_mode == "画像アップロード":
        uploaded_file = st.file_uploader("画像ファイルをアップロード", type=["png", "jpg", "jpeg", "bmp", "gif"], help="名刺・書類・ホワイトボード写真などもOK")
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                input_str = tmp_file.name
    else:
        text = st.text_area("テキストを直接入力", height=180, help="議事録・メモ・メール文なども貼り付け可能")
        if text:
            input_str = text

    st.markdown("---")
    st.markdown(
        "> **注意:** 入力内容は一時的にのみ処理され、保存されません。個人情報・機密情報の入力はご注意ください。",
        unsafe_allow_html=True
    )

    if input_str and st.button("AIで要約・音声化", help="AI要約→音声化まで一括処理"):
        with st.spinner("本文・テキスト抽出中..."):
            article_text = extract_article_text(input_str)
        if article_text.strip().startswith("[エラー]"):
            st.error(article_text)
            return
        st.subheader("抽出テキスト")
        st.info(article_text[:1000] + ("..." if len(article_text) > 1000 else ""))

        with st.spinner("要約・解説生成中..."):
            summary = summarize_article(article_text, config)
        st.subheader("要約・解説")
        st.success(summary)

        with st.spinner("音声合成中..."):
            audio_path = synthesize_speech(summary, config)
        st.subheader("音声再生・ダウンロード")
        audio_bytes = open(audio_path, 'rb').read()
        st.audio(audio_bytes, format='audio/mp3')
        st.download_button("音声ファイルをダウンロード", audio_bytes, file_name="summary.mp3", mime="audio/mp3")
        # 一時ファイル削除
        if input_mode == "画像アップロード" and input_str:
            os.remove(input_str)
        os.remove(audio_path)

if __name__ == "__main__":
    main() 