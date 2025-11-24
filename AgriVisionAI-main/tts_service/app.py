from flask import Flask, request, jsonify
import base64
import io
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

try:
    from google.cloud import texttospeech
except Exception as e:
    texttospeech = None

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/synthesize', methods=['POST'])
def synthesize():
    if texttospeech is None:
        return jsonify({'error': 'google-cloud-texttospeech library not available'}), 500

    data = request.get_json() or {}
    text = data.get('text')
    lang = data.get('lang', 'en')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Map simple codes to locales
    lang_map = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'kn': 'kn-IN',
        'te': 'te-IN',
        'ta': 'ta-IN'
    }
    locale = lang_map.get(lang, lang)

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=locale, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    try:
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        audio_bytes = response.audio_content
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        return jsonify({'audio': audio_b64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6000))
    app.run(host='0.0.0.0', port=port)
