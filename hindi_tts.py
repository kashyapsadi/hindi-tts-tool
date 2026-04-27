import streamlit as st
import edge_tts
import asyncio
import os

# Page config
st.set_page_config(page_title="Indian Voice Selector", page_icon="🎙️")

st.title("🎙️ Indian Accent TTS (Free)")

# Voice options ki list
VOICES = {
    "Madhur (Male - Hindi)": "hi-IN-MadhurNeural",
    "Swara (Female - Hindi)": "hi-IN-SwaraNeural",
    "Prabhat (Male - Indian English/Hinglish)": "en-IN-PrabhatNeural",
    "Neerja (Female - Indian English/Hinglish)": "en-IN-NeerjaNeural"
}

text = st.text_area("Yahan apna Hinglish text likhein:", 
                    placeholder="Dosto, aaj ki kahani bahut bhayanak hai...",
                    height=150)

# Dropdown for selecting voice
selected_voice_name = st.selectbox("Apni pasand ki voice chunein:", list(VOICES.keys()))
selected_voice = VOICES[selected_voice_name]

async def generate_speech(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

if st.button("Generate Audio"):
    if text:
        with st.spinner(f"{selected_voice_name} ki awaaz ban rahi hai..."):
            output_file = "output_audio.mp3"
            asyncio.run(generate_speech(text, selected_voice, output_file))
            
            # Play Audio
            audio_file = open(output_file, 'rb')
            st.audio(audio_file.read(), format='audio/mp3')
            st.success("Audio ready!")
    else:
        st.warning("Pehle text likhein.")

st.info("Tip: 'Prabhat' ya 'Neerja' try karein agar aapka text English words se bhara hai (Hinglish).")