def summarize_article(article_text, config, length=None):
    """
    概要説明: Gemini APIで記事本文を要約・解説する
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
    # TODO: Gemini API連携実装
    prompt = config['ai']['summarization_prompt'] + "\n" + article_text
    # ダミー実装: 指定長で切り出し
    if length is not None:
        summary = article_text[:length]
    else:
        summary = article_text
    return summary 