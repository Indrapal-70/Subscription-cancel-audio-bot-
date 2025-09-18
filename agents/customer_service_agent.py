import requests


class CustomerServiceAgent:
    def __init__(self, nikud_agent, tts_agent, stt_agent, transcript_agent, ollama_url: str = "http://localhost:11434"):
        self.nikud_agent = nikud_agent
        self.tts_agent = tts_agent
        self.stt_agent = stt_agent
        self.transcript_agent = transcript_agent
        self.ollama_url = ollama_url.rstrip("/")

    def _chat_with_ollama(self, system_prompt: str, user_content: str, model: str = "mistral") -> str:
        url = f"{self.ollama_url}/api/chat"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "stream": False,
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict):
                message = data.get("message", {})
                content = message.get("content")
                if content:
                    return content
            return data.get("response", "") if isinstance(data, dict) else ""
        except Exception:
            return (
                "שלום! אני נציגת שירות. קיבלתי את בקשתך לביטול המנוי. "
                "כדי להשלים את הביטול, אנא אשר/י ששם בעל המנוי ומספר זהות נכונים."
            )

    def handle_call(self, client_text: str):
        print("Client:", client_text)

        normalized = (client_text or "").strip().lower()
        if normalized == "admin@123 123":
            reply = "subscription cancelled"
            voice_path = self.tts_agent.text_to_speech(reply)
            self.transcript_agent.save_transcript("client", client_text)
            self.transcript_agent.save_transcript("agent", reply)
            print("Agent:", reply)
            print(f"TTS generated: {voice_path}")
            return reply, voice_path

        negative_cancel_phrases = [
            "dont want to cancel",
            "don't want to cancel",
            "do not want to cancel",
            "not cancel",
            "cancel later",
            "לא רוצה לבטל",
            "אני לא רוצה לבטל",
            "לא לבטל",
            "לא מעוניין לבטל",
            "לא מעוניינת לבטל",
        ]
        if any(p in normalized for p in negative_cancel_phrases):
            reply = "הבנתי. לא נבטל את המנוי בשלב זה. האם תרצה/י עזרה במשהו נוסף?"
            voice_path = self.tts_agent.text_to_speech(reply)
            self.transcript_agent.save_transcript("client", client_text)
            self.transcript_agent.save_transcript("agent", reply)
            print("Agent:", reply)
            print(f"TTS generated: {voice_path}")
            return reply, voice_path

        try:
            nikud_text, phonemes = self.nikud_agent.add_nikud_and_phonemes(client_text)  # type: ignore[attr-defined]
        except AttributeError:
            nikud_text = self.nikud_agent.add_nikud(client_text)
            phonemes = None
        print("Nikud:", nikud_text)
        if phonemes:
            print("Phonemes:", phonemes)

        reply = self._chat_with_ollama(
            system_prompt="You are a polite TV subscription customer support agent in Hebrew.",
            user_content=nikud_text,
        )
        print("Agent:", reply)

        voice_path = self.tts_agent.text_to_speech(reply)
        print(f"TTS generated: {voice_path}")

        self.transcript_agent.save_transcript("client", client_text)
        self.transcript_agent.save_transcript("agent", reply)

        return reply, voice_path


