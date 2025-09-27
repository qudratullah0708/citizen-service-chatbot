from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from Citizen_Input import extract_citizen_data, CitizenProfile
from housing_services import check_housing_eligibility, generate_housing_forms
from banking_services import check_financial_eligibility, calculate_zakat_eligibility
from emergency_services import check_emergency_eligibility, generate_emergency_forms
from dotenv import load_dotenv
from datetime import datetime
import os
import asyncio

import litellm  # needed for classification with Gemini
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

load_dotenv()
set_tracing_disabled(disabled=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

# Validate API key before creating client
if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "":
    print(f"{Fore.RED}[ERROR]: GEMINI_API_KEY is not set or is empty in .env file{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[SOLUTION]: Please add your Gemini API key to the .env file:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}GEMINI_API_KEY=your_gemini_api_key_here{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Get your API key from: https://makersuite.google.com/app/apikey{Style.RESET_ALL}")
    raise ValueError("GEMINI_API_KEY is required but not provided")

# Validate MODEL configuration
if not MODEL or MODEL.strip() == "":
    print(f"{Fore.RED}[ERROR]: MODEL is not set in .env file{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[SOLUTION]: Please add MODEL to the .env file:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MODEL=gemini/gemini-1.5-flash{Style.RESET_ALL}")
    raise ValueError("MODEL is required but not provided")

print(f"{Fore.GREEN}[CONFIG]: Successfully loaded GEMINI_API_KEY and MODEL{Style.RESET_ALL}")

# Configure LiteLLM to use Gemini
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

app = FastAPI(title="Citizen Service Navigator API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://citizen-service-navigator.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

class CitizenQueryRequest(BaseModel):
    query: str
    citizen_data: dict = None

class CitizenProfile(BaseModel):
    name: str
    age: int
    income: float
    family_size: int
    location: str
    existing_benefits: list = []
    emergency_status: str = None

async def classify_service_intent(user_query: str) -> str:
    try:
        # Use LiteLLM with Gemini for classification
        completion = await litellm.acompletion(
            model="gemini/gemini-1.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classifier for citizen services. Given a user query, reply with one word: "
                        "'housing' if the user is asking about housing support, rent assistance, property registration, or LDA services. "
                        "'banking' if the user is asking about financial aid, loans, banking services, or Zakat. "
                        "'emergency' if the user is asking about emergency services, disaster relief, or urgent assistance. "
                        "Or 'general_info' if the user is just asking for general information about available services."
                    )
                },
                {"role": "user", "content": user_query}
            ],
            temperature=0,
            max_tokens=10,
        )
        intent = completion.choices[0].message.content.strip().lower()
        
        # Clean up the response to ensure it's one of our expected values
        valid_intents = ['housing', 'banking', 'emergency', 'general_info']
        for valid_intent in valid_intents:
            if valid_intent in intent:
                intent = valid_intent
                break
        else:
            intent = 'general_info'  # Default fallback
        
        print(f"{Fore.YELLOW}[SERVICE INTENT CLASSIFIED]: {intent}{Style.RESET_ALL}")
        return intent
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Classification failed: {e}{Style.RESET_ALL}")
        return 'general_info'  # Default fallback

general_info_agent = Agent(
    name="General Info Agent",
    instructions=(
        "Answer the user's question about available citizen services in a helpful and concise way. "
        "Mention housing support, financial aid, emergency services, and other available programs. "
        "Do not assume they want to apply for anything specific. Provide general guidance about eligibility and next steps."
    ),
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

housing_agent = Agent(
    name="Housing Services Agent",
    instructions=(
        "You are a housing services specialist. Use the available tools to check housing eligibility, "
        "generate housing application forms, and provide guidance on housing support programs. "
        "Focus on LDA services, rent assistance, and property registration. "
        "Provide clear explanations of eligibility criteria and required documents."
    ),
    tools=[check_housing_eligibility, generate_housing_forms],
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

banking_agent = Agent(
    name="Banking Services Agent", 
    instructions=(
        "You are a banking and financial services specialist. Use the available tools to check financial eligibility, "
        "calculate Zakat eligibility, and provide guidance on financial aid programs. "
        "Focus on income-based assistance, loans, and Zakat distribution. "
        "Provide clear explanations of financial criteria and application processes."
    ),
    tools=[check_financial_eligibility, calculate_zakat_eligibility],
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

emergency_agent = Agent(
    name="Emergency Services Agent",
    instructions=(
        "You are an emergency services specialist. Use the available tools to check emergency eligibility, "
        "generate emergency assistance forms, and provide guidance on emergency services. "
        "Focus on disaster relief, urgent assistance, and crisis support. "
        "Prioritize immediate needs and provide clear next steps for emergency situations."
    ),
    tools=[check_emergency_eligibility, generate_emergency_forms],
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

@app.post("/citizen-service")
async def citizen_service(request: CitizenQueryRequest):
    user_query = request.query
    print(f"{Fore.CYAN}[CITIZEN REQUEST RECEIVED]: {user_query}{Style.RESET_ALL}")

    intent = await classify_service_intent(user_query)

    if intent == "general_info":
        print(f"{Fore.CYAN}[GENERAL INFO AGENT]: Running…{Style.RESET_ALL}")
        response = await Runner.run(general_info_agent, user_query)
        print(f"{Fore.GREEN}[GENERAL INFO RESPONSE]:\n{response.final_output}{Style.RESET_ALL}")
        return {
            "intent": intent,
            "response": response.final_output
        }

    print(f"{Fore.CYAN}[CITIZEN SERVICE]: Extracting and validating citizen data…{Style.RESET_ALL}")
    try:
        extracted_data = extract_citizen_data(user_query, request.citizen_data)
        validated = CitizenProfile(**extracted_data)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {e}{Style.RESET_ALL}")
        raise HTTPException(status_code=400, detail=str(e))

    citizen_name = extracted_data["name"]
    citizen_age = extracted_data["age"]
    citizen_income = extracted_data["income"]
    family_size = extracted_data["family_size"]
    location = extracted_data["location"]
    existing_benefits = extracted_data["existing_benefits"]
    emergency_status = extracted_data.get("emergency_status")

    # Intelligent supervisor - call only the relevant agent based on intent
    async def intelligent_supervisor():
        print(f"{Fore.CYAN}[INTELLIGENT SUPERVISOR]: Determining appropriate agent for {intent} service…{Style.RESET_ALL}")
        
        # Select the appropriate agent based on intent
        if intent == "housing":
            selected_agent = housing_agent
            agent_name = "Housing Services Agent"
            tools_description = "housing eligibility and form generation"
        elif intent == "banking":
            selected_agent = banking_agent
            agent_name = "Banking Services Agent"
            tools_description = "financial eligibility and Zakat calculation"
        elif intent == "emergency":
            selected_agent = emergency_agent
            agent_name = "Emergency Services Agent"
            tools_description = "emergency eligibility and assistance forms"
        else:
            raise HTTPException(status_code=400, detail=f"Invalid service intent: {intent}")
        
        print(f"{Fore.CYAN}[{agent_name.upper()}]: Running with {tools_description}…{Style.RESET_ALL}")
        
        # Run only the selected agent
        agent_result = await Runner.run(selected_agent, f"Assist citizen {citizen_name} with {intent} services")
        
        print(f"{Fore.GREEN}[{agent_name.upper()} RESULT]:\n{agent_result.final_output}{Style.RESET_ALL}")
        
        # Create a comprehensive response agent to provide additional context
        comprehensive_agent = Agent(
            name="Comprehensive Response Agent",
            instructions=(
                f"Provide comprehensive guidance for {citizen_name} regarding {intent} services. "
                f"Citizen Profile: Age {citizen_age}, Income Rs. {citizen_income:,.2f}, "
                f"Family Size {family_size}, Location {location}. "
                f"Existing Benefits: {existing_benefits}. "
                f"Emergency Status: {emergency_status or 'None'}. "
                f"Based on the {agent_name} results, provide additional context about: "
                f"1. Related services that might benefit this citizen "
                f"2. Next steps and follow-up actions "
                f"3. Important contacts and resources "
                f"4. Tips for successful application "
                f"Use plain language and provide actionable advice."
            ),
            model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        )
        
        print(f"{Fore.CYAN}[COMPREHENSIVE RESPONSE AGENT]: Running…{Style.RESET_ALL}")
        comprehensive_result = await Runner.run(comprehensive_agent, f"Provide comprehensive {intent} service guidance for citizen {citizen_name}")
        
        print(f"{Fore.GREEN}[COMPREHENSIVE RESPONSE]:\n{comprehensive_result.final_output}{Style.RESET_ALL}")
        
        return {
            "intent": intent,
            "citizen_data": validated.model_dump(),
            "primary_service": agent_result.final_output,
            "comprehensive_guidance": comprehensive_result.final_output,
            "offline_mode": await get_degraded_response(validated, intent)
        }
    
    result = await intelligent_supervisor()
    return result

async def get_degraded_response(citizen_data: CitizenProfile, service_intent: str) -> dict:
    """Provide offline/degraded mode response when real-time services are unavailable"""
    return {
        "status": "offline_mode",
        "message": "Real-time services unavailable. Using cached eligibility rules.",
        "service_type": service_intent,
        "basic_guidance": f"Based on your profile (Income: Rs. {citizen_data.income:,.2f}, Family: {citizen_data.family_size}), you may be eligible for {service_intent} services.",
        "next_steps": f"Visit your local {service_intent} service center or call the helpline for detailed assistance.",
        "emergency_contact": "For emergencies, call 112 or visit the nearest emergency service center."
    }