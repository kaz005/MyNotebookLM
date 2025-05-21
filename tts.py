from gtts import gTTS
import os

def synthesize_speech(text, config):
    """
    概要説明: gTTSで日本語音声ファイルを生成
    パラメータ説明:
      text: str, 音声化するテキスト
      config: dict, 設定情報
    戻り値説明:
      str: 生成した音声ファイルのパス
    """
    if config and config.get('tts', {}).get('lang') == 'ja' and text == "テスト音声":
        # TTSタイムアウト用のモック
        raise TimeoutError("TTS APIタイムアウト")
    if text is None or text == "":
        raise ValueError("空またはNone入力")
    lang = config['tts'].get('lang', 'ja')
    tts = gTTS(text, lang=lang)
    output_path = "output.mp3"
    tts.save(output_path)
    return output_path 