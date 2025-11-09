# import streamlit as st
# import speech_recognition as sr
# import pyttsx3

# # -------------------------------------------------
# # Dummy Function (replace later with real AI logic)
# # -------------------------------------------------
# def get_bot_response(query: str) -> str:
#     # Simulate AI answering (dummy response)
#     return f" aaa You asked: '{query}'. This is your dummy AI speaking confidently like Vjeet!"

# # -------------------------------------------------
# # Text-to-Speech Function (Male Voice)
# # -------------------------------------------------
# def speak_text(answer):
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')

#     # Try to select a male voice
#     male_voice_found = False
#     for voice in voices:
#         if "male" in voice.name.lower() or "david" in voice.name.lower():
#             engine.setProperty('voice', voice.id)
#             male_voice_found = True
#             break

#     if not male_voice_found and voices:
#         # Default to first voice if male not found
#         engine.setProperty('voice', voices[0].id)

#     engine.setProperty('rate', 160)  # speaking speed
#     engine.say(answer)
#     engine.runAndWait()
#     engine.stop()

# # -------------------------------------------------
# # Streamlit App UI
# # -------------------------------------------------
# st.set_page_config(page_title="Vjeet's Voice Interview Bot", page_icon="🎙️", layout="centered")

# st.title("🎙️ Vjeet's Voice Interview Bot")
# st.markdown("""
# Welcome!  
# I'm **Vjeet's AI voice assistant**, here to answer interview-style questions about him.  
# Click below to speak your question — I’ll respond in a **male human-like voice** 🎧
# """)

# r = sr.Recognizer()

# # 🎤 Voice Input Button
# if st.button("🎧 Start Recording"):
#     with st.spinner("Listening... please speak now 🎤"):
#         try:
#             with sr.Microphone() as source:
#                 r.adjust_for_ambient_noise(source)
#                 audio = r.listen(source, timeout=6)
#                 st.info("Processing your voice...")
#                 query = r.recognize_google(audio)
#                 st.success(f"🗣️ You said: {query}")
#         except sr.UnknownValueError:
#             st.error("Sorry, I couldn’t understand. Please try again.")
#             query = ""
#         except sr.RequestError:
#             st.error("Speech recognition service is unavailable right now.")
#             query = ""
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#             query = ""

#     # ✅ If voice recognized successfully
#     if query:
#         answer = get_bot_response(query)
#         st.write("🤖 **Bot:**", answer)

#         # Speak the response
#         st.write("🔊 Speaking...")
#         speak_text(answer)
#         st.success("✅ Done speaking!")

# # 💬 Fallback Text Input
# st.divider()
# st.write("💬 Or type your question below (if mic doesn’t work):")
# user_text = st.text_input("Type here...")

# if user_text:
#     answer = get_bot_response(user_text)
#     st.write("🤖 **Bot:**", answer)
#     st.write("🔊 Speaking...")
#     speak_text(answer)
#     st.success("✅ Done speaking!")

# st.markdown("---")
# st.caption("Developed by **Vjeet Shekhawat** | Free Offline Version for 100x AI Voice Interview Assessment")






import streamlit as st
import speech_recognition as sr
import asyncio
from gtts import gTTS

from first import get_model_response 
# -------------------------------------------------
# Dummy Function
# -------------------------------------------------

# def get_bot_response(query: str) -> str:
#     return f" Hmm You asked: '{query}'. This is your dummy AI speaking confidently like Vjeet!"

# -------------------------------------------------   
# Edge TTS (Male Voice) – Saves file & plays in browser
# -------------------------------------------------   
# async def speak_text(answer):
#     voice = "en-US-ChristopherNeural"  # deeper male voice
#     rate = "-10%"                      # slower, confident
#     pitch = "-5Hz"                     # deeper tone
#     file_path = "response.mp3"
#     tts = edge_tts.Communicate(answer, voice=voice, rate=rate, pitch=pitch)
#     # ssml_text = """
#     # <speak>
#     #     <prosody rate="-10%" pitch="-5Hz" volume="+10%">Hmm...</prosody>
#     #     <break time="300ms"/>
#     #     <prosody rate="-5%" pitch="-3Hz">That’s an interesting question!</prosody>
#     # </speak>
#     # """
#     # tts = edge_tts.Communicate(ssml_text, voice="en-US-ChristopherNeural")
#     await tts.save(file_path)
#     return file_path


async def speak_text(answer):
    file_path = "response.mp3"
    loop = asyncio.get_event_loop()
    # run blocking gTTS in a thread
    await loop.run_in_executor(None, lambda: gTTS(text=answer, lang='en').save(file_path))
    return file_path

# -------------------------------------------------
# Streamlit App
# ------------------------------------------------- 

st.set_page_config(page_title="Vjeet's Voice Interview Bot", page_icon="🎙️")

st.title("🎙️ Vishvajeet's Voice Interview Bot")
st.write("")

r = sr.Recognizer()

if st.button("🎧 Start Recording"):
    with st.spinner("Listening..."):
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=6)
                st.info("Processing your voice...")
                query = r.recognize_google(audio)
                st.success(f"🗣️ You said: {query}")
        except Exception as e:
            st.error(f"Error: {e}")
            query = ""

    if query:
        answer = get_model_response(query)
        st.write("🤖 **Bot:**", answer)

        st.write("🔊 Generating voice...")
        file_path = asyncio.run(speak_text(answer))

        st.audio(file_path, format="audio/mp3")

st.divider()
text = st.text_input("💬 Or type your question:")
if text:
    answer = get_model_response(text)
    st.write("🤖 **Bot:**", answer)
    file_path = asyncio.run(speak_text(answer))
    st.audio(file_path, format="audio/mp3")

st.markdown("---")
st.caption("Developed by **Vjeet Shekhawat** | Uses free Microsoft Neural Voices for natural speech")
