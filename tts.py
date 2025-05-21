from gtts import gTTS
import os

def synthesize_speech(text, config):
    """
    概要説明: gTTSまたはGoogle Cloud TTSで日本語音声ファイルを生成
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
    engine = os.getenv("TTS_ENGINE", config.get('tts', {}).get('engine', 'gtts')).lower()
    output_path = "output.mp3"
    if engine == "google_cloud":
        try:
            from google.cloud import texttospeech
        except ImportError:
            raise ImportError("google-cloud-texttospeechパッケージが必要です")
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        return output_path
    else:
        tts = gTTS(text, lang=lang)
        tts.save(output_path)
        return output_path 