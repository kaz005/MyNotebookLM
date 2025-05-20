def summarize_article(article_text, config):
    """
    概要説明: Gemini APIで記事本文を要約・解説する
    パラメータ説明:
      article_text: str, 記事本文
      config: dict, 設定情報
    戻り値説明:
      str: 要約・解説テキスト
    """
    # TODO: Gemini API連携実装
    prompt = config['ai']['summarization_prompt'] + "\n" + article_text
    # 仮実装: 本文をそのまま返す
    return f"[要約・解説(ダミー)]\n{article_text}" 