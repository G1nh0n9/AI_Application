import base64
import streamlit as st
from openai import OpenAI
import datetime

client = OpenAI()

# 관리 패널 (사이드바)
with st.sidebar:
    st.header("🎧 Audio Management Panel")
    enable_audio_save = st.checkbox("Enable Audio Download", value=False)
    
    if enable_audio_save:
        st.info("📁 Audio download enabled")
        st.caption("Download buttons will appear next to audio elements")

# 음성 입력
st.header("🎤 Voice Input")
audio = st.audio_input("Record your voice:")

# 입력 오디오 다운로드 버튼
if audio and enable_audio_save:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 Download Input Audio",
        data=audio.getvalue(),
        file_name=f"input_audio_{timestamp}.wav",
        mime="audio/wav"
    )

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

        # 일본어 음성 생성
        st.header("🔊 Japanese Audio Output")
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
        
        # 출력 오디오 다운로드 버튼
        if enable_audio_save:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 Download Japanese Audio (MP3)",
                data=answer.content,
                file_name=f"japanese_audio_{timestamp}.mp3",
                mime="audio/mp3"
            )