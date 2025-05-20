import sys
import yaml
from summarizer import summarize_article
from tts import synthesize_speech
from extractor import extract_article_text


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    if len(sys.argv) < 2:
        print("使い方: python main.py <URLまたは画像ファイルパスまたはテキスト>")
        sys.exit(1)
    input_str = sys.argv[1]
    print(f"入力: {input_str}")

    # 1. 本文またはテキスト抽出
    article_text = extract_article_text(input_str)
    print("\n--- 抽出テキスト ---\n")
    print(article_text[:500] + ("..." if len(article_text) > 500 else ""))

    # 2. 要約・解説生成
    summary = summarize_article(article_text, config)
    print("\n--- 要約・解説 ---\n")
    print(summary)

    # 3. 音声合成
    audio_path = synthesize_speech(summary, config)
    print(f"\n音声ファイル生成: {audio_path}")

if __name__ == "__main__":
    main() 