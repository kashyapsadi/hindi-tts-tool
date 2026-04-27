import streamlit as st
import edge_tts
import asyncio
import os

st.set_page_config(page_title="Universal Hindi/Hinglish TTS", page_icon="🎙️")
st.title("🎙️ Hindi & Hinglish Voice Tool")

# Voices selection logic
VOICES = {
    "Madhur (Hindi/Hinglish - Male)": "hi-IN-MadhurNeural",
    "Swara (Hindi/Hinglish - Female)": "hi-IN-SwaraNeural",
    "Prabhat (Best for pure Hinglish - Male)": "en-IN-PrabhatNeural",
}

text = st.text_area("Yahan apni kahani likhein (Hindi script ya Hinglish dono chalega):", 
                    placeholder="Example: एक पुरानी कहानी... ya 'Ek purani kahani...'",
                    height=200)

selected_voice_name = st.selectbox("Awaaz chunein:", list(VOICES.keys()))
selected_voice = VOICES[selected_voice_name]

async def generate_speech(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    # Stream method is more stable for long scripts
    found_audio = False
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            with open(output_file, "ab") as f:
                f.write(chunk["data"])
                found_audio = True
    return found_audio

if st.button("Generate Audio"):
    if text.strip():
        with st.spinner("Processing... thoda samay dein"):
            output_file = "final_voice.mp3"
            
            if os.path.exists(output_file):
                os.remove(output_file)
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success = loop.run_until_complete(generate_speech(text, selected_voice, output_file))
                
                if success:
                    st.audio(output_file, format='audio/mp3')
                    st.success("Aapki awaaz taiyar hai!")
                    with open(output_file, "rb") as f:
                        st.download_button("Audio Download Karein", f, file_name="story.mp3")
                else:
                    st.error("Audio generate nahi ho paya. Try changing the script style.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle kuch likhiye!")

st.info("💡 Tip: Agar aapne 'देवनागरी' (Hindi) mein likha hai, toh 'Madhur' ya 'Swara' best results denge.")
