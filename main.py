import requests
from Extractor import extractor_developer_profile

LLAMA_CPP_URL = "http://localhost:8080/v1/chat/completions"

def run_chat_intake():
    print("Welcome to the Developer & Tech Profile Intake Assistant")
    print("Chat naturally with the assistant to set up your profile.")
    print("Type 'quit' or 'exit' at any time to end the session.\n")

    system_prompt = (
        "You are a friendly, professional technical recruiter and onboarding assistant. "
        "Your goal is to converse with the user and collect their professional details: "
        "full name, age, professional email, primary role (Full-Stack Developer, Web Developer, "
        "Prompt Engineer, AI Agent), experience level (Junior, Mid, Senior), their tech stack "
        "technologies, and account type (professional or enterprise). If account type is enterprise, "
        "you must also ask for their company name. "
        "Have a natural conversation, ask for missing details organically one or two at a time, "
        "and do NOT interrogate them all at once. "
        "CRITICAL RULE: The moment you have successfully gathered ALL required information "
        "(name, age, email, role, experience level, tech stack, account type, and company name if enterprise), "
        "your response MUST start with the exact phrase 'Thank you!' followed by a brief wrap-up message confirming "
        "that their profile has been successfully captured."
    )
    
    chat_history = [{"role": "system", "content": system_prompt}]    
        
    initial_greeting_payload = {
        "model": "local-model",
        "messages": chat_history,
        "temperature": 0.7,
        "stream": False
    }

    try:
        print("Assistant is ready...")
        
        response = requests.post(LLAMA_CPP_URL, json=initial_greeting_payload, timeout=60)
        response.raise_for_status()
        assistant_message = response.json()["choices"][0]["message"]["content"]

        print(f"\nAssistant: {assistant_message}")
        
        chat_history.append({"role": "assistant", "content": assistant_message})

    except requests.exceptions.ConnectionError:  # Fixed: requests.exceptions (plural)
        print("\n[ERROR]: Could not connect to local llama.cpp server. Make sure it is running on port 8080!")
        return
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        return

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):  
            print("\nExiting session. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit"]:
            print("\nSession ended by user.Goodbye!")
            break

        chat_history.append({"role": "user", "content": user_input})

        payload = {
            "model": "local-model",
            "messages": chat_history,  
            "temperature": 0.7,
            "stream": False  
        }

        try:
            
            response = requests.post(LLAMA_CPP_URL, json=payload, timeout=60)
            response.raise_for_status()  

            assistant_message = response.json()["choices"][0]["message"]["content"]
            print(f"\nAssistant: {assistant_message}")

    
            chat_history.append({"role": "assistant", "content": assistant_message})

            # Check if assistant triggered the closing sign-off
            if assistant_message.strip().startswith("Thank you!"):
                print("\n" + "=" * 50)
                print("Intake completed! Triggering automated extraction pipeline...")
                print("=" * 50)

                # Call your extractor function and pass the chat history
                profile = extract_developer_profile(chat_history)

                print("\nSuccessfully extracted and validated!")
                print(profile.model_dump_json(indent=2))
                print("\nYour profile is pristine and ready for database insertion.")
                break

        except requests.exceptions.ConnectionError:
            print("\n[ERROR]: Lost connection to local llama.cpp server.")
            break
        except Exception as e:  
            print(f"\n[ERROR]: {e}")  

if __name__ == "__main__":  
    run_chat_intake()
