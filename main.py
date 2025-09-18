from crew_flow import create_crew_flow


if __name__ == "__main__":
    customer_service, client = create_crew_flow()

    client_text = client.speak()
    customer_service.handle_call(client_text)

    print("Conversation finished. Transcript saved in transcript.txt")


