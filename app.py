import os
import tempfile

import streamlit as st

from crew_flow import create_crew_flow


st.set_page_config(page_title="Hebrew Customer Service", page_icon="📞", layout="centered")
st.title("Hebrew Customer Service Demo")
st.caption("Text → Nikud → LLM reply → TTS. Upload WAV audio to transcribe.")


@st.cache_resource(show_spinner=False)
def init_agents():
    customer_service, client = create_crew_flow()
    return customer_service, client, customer_service.nikud_agent, customer_service.tts_agent, customer_service.stt_agent, customer_service.transcript_agent


customer_service, _client, nikud_agent, tts_agent, stt_agent, transcript_agent = init_agents()

tab_text, tab_audio = st.tabs(["Text Input", "Audio Upload (WAV)"])

with tab_text:
    st.subheader("Enter text in Hebrew")
    user_text = st.text_area("Your message", value="אני רוצה לבטל את המנוי שלי לאינטרנט", height=120)
    if st.button("Send", type="primary"):
        if not user_text.strip():
            st.warning("Please enter some text.")
        else:
            try:
                try:
                    nikud_text, phonemes = nikud_agent.add_nikud_and_phonemes(user_text)  # type: ignore[attr-defined]
                except AttributeError:
                    nikud_text = nikud_agent.add_nikud(user_text)
                    phonemes = None

                st.write("**Nikud:**")
                st.write(nikud_text)
                if phonemes:
                    st.write("**Phonemes:**")
                    st.write(phonemes)

                reply, voice_path = customer_service.handle_call(user_text)

                st.write("**Agent reply:**")
                st.write(reply)

                if os.path.exists(voice_path):
                    with open(voice_path, "rb") as f:
                        st.audio(f.read(), format="audio/mp3" if voice_path.lower().endswith(".mp3") else "audio/wav")
                    st.success(f"Voice saved: {voice_path}")
                else:
                    st.info("Voice file not found.")

                st.write("**Transcript (latest):**")
                if os.path.exists(transcript_agent.filename):
                    with open(transcript_agent.filename, "r", encoding="utf-8") as f:
                        st.code(f.read(), language="text")
            except Exception as e:
                st.error(f"Error: {e}")

with tab_audio:
    st.subheader("Upload a WAV file (mono, 16kHz recommended)")
    wav_file = st.file_uploader("Choose a WAV file", type=["wav"]) 
    if wav_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(wav_file.read())
            tmp_path = tmp.name

        st.audio(wav_file, format="audio/wav")

        if st.button("Transcribe & Respond", key="transcribe"):
            try:
                text = stt_agent.speech_to_text(tmp_path)
                st.write("**Transcribed text:**")
                st.write(text or "(empty)")

                if text.strip():
                    try:
                        nikud_text, phonemes = nikud_agent.add_nikud_and_phonemes(text)  # type: ignore[attr-defined]
                    except AttributeError:
                        nikud_text = nikud_agent.add_nikud(text)
                        phonemes = None

                    st.write("**Nikud:**")
                    st.write(nikud_text)
                    if phonemes:
                        st.write("**Phonemes:**")
                        st.write(phonemes)

                    reply, voice_path = customer_service.handle_call(text)
                    st.write("**Agent reply:**")
                    st.write(reply)

                    if os.path.exists(voice_path):
                        with open(voice_path, "rb") as f:
                            st.audio(f.read(), format="audio/mp3" if voice_path.lower().endswith(".mp3") else "audio/wav")
                        st.success(f"Voice saved: {voice_path}")
                else:
                    st.info("No text transcribed.")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

st.sidebar.header("About")
st.sidebar.markdown(
    "This demo runs locally using Phonikud (ONNX) for diacritics, optional Vosk for STT, "
    "and gTTS for audio playback. If Ollama is not running, a default Hebrew reply is used."
)


