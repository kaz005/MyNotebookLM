import os
import openai

# Gemini用のimportは将来用
# import google.generativeai as genai

def summarize_article(article_text, config, length=None):
    """
    概要説明: Gemini/OpenAI APIで記事本文を要約・解説する
    パラメータ説明:
      article_text: str, 記事本文
      config: dict, 設定情報
      length: int, 要約の長さ（文字数）
    戻り値説明:
      str: 要約・解説テキスト
    """
    # 入力バリデーション
    if article_text is None or article_text == "":
        raise ValueError("入力テキストが空です")
    if length is not None and len(article_text) > 100000:
        raise ValueError("入力テキストが最大長を超えています")

    # APIスイッチ判定
    use_dummy = os.getenv("USE_DUMMY_API", "false").lower() == "true"
    engine = os.getenv("SUMMARIZER_ENGINE", config.get('ai', {}).get('summarizer_engine', 'dummy')).lower()
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"[DEBUG] use_dummy={use_dummy}, engine={engine}, OPENAI_API_KEY={'set' if api_key else 'unset'}")
    if use_dummy or engine == "dummy":
        if length is not None:
            return f"[要約ダミー] {article_text[:length]}"
        else:
            return f"[要約ダミー] {article_text}"
    elif engine == "openai":
        # OpenAI GPT-4.1-nanoによる要約
        if not api_key:
            raise RuntimeError("OPENAI_API_KEYが設定されていません")
        openai.api_key = api_key
        prompt = f"以下の文章を日本語で{length or 200}文字以内に要約してください。\n\n" + article_text
        try:
            response = openai.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "あなたは優秀な日本語要約AIです。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=length or 200,
                temperature=0.3,
            )
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            return f"[OpenAI要約エラー] {str(e)}"
    elif engine == "gemini":
        # TODO: Gemini API連携（将来実装）
        return "[Gemini要約ダミー] " + (article_text[:length] if length else article_text)
    else:
        return f"[要約エンジン未対応: {engine}] {article_text[:length] if length else article_text}" 