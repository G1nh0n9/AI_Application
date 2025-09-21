import base64
import streamlit as st
from openai import OpenAI

client = OpenAI()
audio = st.audio_input("Record your voice:")

if audio:
    button = st.button("Send a Message")
    if button:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
        )
        st.chat_message("user").write(transcript.text)
        
        # Translation to Japanese
        translation_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
            {"role": "system", "content": "You are a professional translator. Translate the following text to Japanese. Only respond with the translation, no additional text."},
            {"role": "user", "content": transcript.text}
            ],
        )
        
        translated_text = translation_response.choices[0].message.content
        st.chat_message("ai").write(f"Japanese Translation: {translated_text}")

        answer = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=translated_text,
        )
        b64_audio = base64.b64encode(answer.content).decode()

        # 오디오 플레이어 추가 (처음 한번 자동재생, 이후 수동 재생 가능)
        st.html(f"""
                <audio controls autoplay>
                    <source src="data:audio/mpeg;base64,{b64_audio}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
        """)