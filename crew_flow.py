from agents.nikud_agent import NikudAgent
from agents.tts_agent import TTSAgent
from agents.stt_agent import STTAgent
from agents.customer_service_agent import CustomerServiceAgent
from agents.client_agent import ClientAgent
from agents.transcript_agent import TranscriptAgent


def create_crew_flow():
    nikud_agent = NikudAgent()
    tts_agent = TTSAgent()
    stt_agent = STTAgent()
    transcript_agent = TranscriptAgent()

    customer_service = CustomerServiceAgent(
        nikud_agent, tts_agent, stt_agent, transcript_agent
    )
    client = ClientAgent()

    return customer_service, client


