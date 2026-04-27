import streamlit as st
import edge_tts
import asyncio
import os

st.set_page_config(page_title="Hindi/Hinglish TTS", page_icon="🎙️")
st.title("🎙️ Hindi & Hinglish Voice Tool")

VOICES = {
    "Madhur (Hindi/Hinglish - Male)": "hi-IN-MadhurNeural",
    "Swara (Hindi/Hinglish - Female)": "hi-IN-SwaraNeural",
    "Prabhat (Hinglish ONLY - Male)": "en-IN-PrabhatNeural",
    "Neerja (Female - Indian English/Hinglish)": "en-IN-NeerjaNeural"
}

text = st.text_area("Paste your story here:", height=500)
selected_voice_name = st.selectbox("Select Voice:", list(VOICES.keys()))
selected_voice = VOICES[selected_voice_name]

async def generate_speech(text, voice):
    # Direct memory se byte stream nikalenge
    communicate = edge_tts.Communicate(text, voice)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

if st.button("Generate Audio"):
    if text.strip():
        # Quick validation
        if selected_voice.startswith("en-") and any(ord(c) > 128 for c in text):
            st.error("Error: 'Prabhat' can't read hindi script. Please choose 'Madhur' or 'Swara' .")
        else:
            with st.spinner("Processing..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    audio_bytes = loop.run_until_complete(generate_speech(text, selected_voice))
                    
                    if audio_bytes:
                        st.audio(audio_bytes, format='audio/mp3')
                        st.download_button("Download MP3", audio_bytes, file_name="story.mp3")
                    else:
                        st.error("Audio received nahi hua. Script badal kar dekhein.")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.warning("Enter Something.")
