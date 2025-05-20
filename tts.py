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
    lang = config['tts'].get('lang', 'ja')
    tts = gTTS(text, lang=lang)
    output_path = "output.mp3"
    tts.save(output_path)
    return output_path 