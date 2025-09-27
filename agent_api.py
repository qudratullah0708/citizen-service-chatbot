from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from Agent_Input import extract_query_data, AccommodationRequest
from airbnb_scraper import scrape_airbnb
from Research_dest import research_destination
from dotenv import load_dotenv
from datetime import datetime
import os
import asyncio

from groq import Groq  # needed for classification
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

load_dotenv()
set_tracing_disabled(disabled=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="Travel Planner API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://trail-mate-ai-agent-fok3.vercel.app",
    "https://trail-mate-ai-agent-7sgi.vercel.app"
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
class QueryRequest(BaseModel):
    query: str


async def classify_intent(user_query: str) -> str:
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a classifier. Given a user query, reply with one word: "
                    "'trip_planning' if the user is asking to plan/book a trip with details like destination, dates, guests, budget, etc. "
                    "Or 'general_info' if the user is just asking for information or advice without booking."
                )
            },
            {"role": "user", "content": user_query}
        ],
        temperature=0,
        max_completion_tokens=10,
    )
    intent = completion.choices[0].message.content.strip()
    print(f"{Fore.YELLOW}[INTENT CLASSIFIED]: {intent}{Style.RESET_ALL}")
    return intent


general_info_agent = Agent(
    name="General Info Agent",
    instructions=(
        "Answer the user's question about travel in a helpful and concise way. "
        "Do not assume they want to book anything. If relevant, mention attractions, best times to visit, culture, or travel tips."
    ),
    model=LitellmModel(model=MODEL, api_key=GROQ_API_KEY),
)


@app.post("/plan-trip")
async def plan_trip(request: QueryRequest):
    user_query = request.query
    print(f"{Fore.CYAN}[REQUEST RECEIVED]: {user_query}{Style.RESET_ALL}")

    intent = await classify_intent(user_query)

    if intent == "general_info":
        print(f"{Fore.CYAN}[GENERAL INFO AGENT]: Running…{Style.RESET_ALL}")
        response = await Runner.run(general_info_agent, user_query)
        print(f"{Fore.GREEN}[GENERAL INFO RESPONSE]:\n{response.final_output}{Style.RESET_ALL}")
        return {
            "intent": intent,
            "response": response.final_output
        }

    print(f"{Fore.CYAN}[TRIP PLANNING]: Extracting and validating data…{Style.RESET_ALL}")
    try:
        extracted_data = extract_query_data(user_query)
        validated = AccommodationRequest(**extracted_data)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {e}{Style.RESET_ALL}")
        raise HTTPException(status_code=400, detail=str(e))

    destination = extracted_data["destination"]
    check_in_str = extracted_data['check_in']
    check_out_str = extracted_data['check_out']
    guests = extracted_data["guests"]
    preferences = extracted_data["standard"]
    min_total_budget = extracted_data["min_budget"]
    max_total_budget = extracted_data["max_budget"]

    check_in_date = datetime.fromisoformat(check_in_str)
    check_out_date = datetime.fromisoformat(check_out_str)
    num_nights = (check_out_date - check_in_date).days
    if num_nights <= 0:
        raise HTTPException(status_code=400, detail="Check-out date must be after check-in date.")

    duration = f"{num_nights} nights ({check_in_str} to {check_out_str})"
    accommodation_budget_ratio = 0.6
    max_accom_budget = max_total_budget * accommodation_budget_ratio
    max_nightly_price = int(max_accom_budget / num_nights)

    experience_planner = Agent(
        name="Experience Planner Agent",
        instructions=(
            f"Use the `research_destination` tool to research and suggest engaging, "
            f"local, and culturally relevant activities and attractions in {destination}. "
            f"The tool only requires the destination name as input. "
            f"After getting the results, analyze and recommend activities suitable for {guests} guest(s) "
            f"for a {duration} trip. The total budget for the trip (accommodations and activities) is ${min_total_budget}-${max_total_budget}. "
            f"The user has a preference for '{preferences}' level experiences. "
            f"Include a variety of options for adventure, relaxation, and sightseeing with estimated costs per person."
        ),
        tools=[research_destination],
        model=LitellmModel(model=MODEL, api_key=GROQ_API_KEY),
    )

    accommodation_agent = Agent(
        name="Accommodation Agent",
        instructions=(
            f"Use the `scrape_airbnb` tool to find available accommodation options. "
            f"The tool requires these parameters: location='{destination}', guests={guests}, "
            f"max_price={max_nightly_price}, check_in='{check_in_str}', check_out='{check_out_str}'. "
            f"Call the tool with these exact parameters. "
            f"Analyze and rank results based on price, guest ratings, proximity to attractions, and overall value. "
            f"Return up to 5 of the best options with clear reasoning for {preferences} preferences."
        ),
        tools=[scrape_airbnb],
        model=LitellmModel(model=MODEL, api_key=GROQ_API_KEY),
    )

    budget_optimizer = Agent(
        name="Budget Optimizer Agent",
        instructions=(
            f"Optimize the trip plan for {guests} guest(s) in {destination} for {duration}. "
            f"The total budget for the trip is between ${min_total_budget} and ${max_total_budget}. "
            f"The user's preference is '{preferences}'. "
            f"Create a day-by-day itinerary with specific costs for activities and accommodation. "
            f"Provide a final summary of the total estimated cost and confirm it fits within the budget. "
            f"IMPORTANT: Format your response using proper Markdown syntax with headers (##), bold text (**text**), "
            f"bullet points (-), and tables. Create a clear cost breakdown table with columns for Day, Activity, and Cost."
        ),
        model=LitellmModel(model=MODEL, api_key=GROQ_API_KEY),
    )

    async def supervisor():
        print(f"{Fore.CYAN}[EXPERIENCE PLANNER]: Running…{Style.RESET_ALL}")
        planner_task = Runner.run(experience_planner, destination)

        print(f"{Fore.CYAN}[ACCOMMODATION AGENT]: Running…{Style.RESET_ALL}")
        accom_task = Runner.run(accommodation_agent, "Find accommodations for the specified parameters in the instructions")

        planner_result, accommodation_result = await asyncio.gather(planner_task, accom_task)

        print(f"{Fore.GREEN}[EXPERIENCE PLANNER RESULT]:\n{planner_result.final_output}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[ACCOMMODATION RESULT]:\n{accommodation_result.final_output}{Style.RESET_ALL}")

        combined_input = (
            f"Trip Planning Data for {destination} ({duration}):\n"
            f"Guests: {guests} | Total Trip Budget: ${min_total_budget}-${max_total_budget} | Standard: {preferences}\n\n"
            f"ACTIVITIES RESEARCH:\n{planner_result.final_output}\n\n"
            f"ACCOMMODATION OPTIONS:\n{accommodation_result.final_output}\n\n"
            f"Please create an optimized itinerary that combines the best activities and accommodation "
            f"within the specified budget. Include a day-by-day cost breakdown and a final total."
        )

        print(f"{Fore.CYAN}[BUDGET OPTIMIZER]: Running…{Style.RESET_ALL}")
        budget_result = await Runner.run(budget_optimizer, combined_input)

        print(f"{Fore.GREEN}[BUDGET OPTIMIZER RESULT]:\n{budget_result.final_output}{Style.RESET_ALL}")

        return {
            "intent": intent,
            "extracted_data": validated.model_dump(),
            "activities": planner_result.final_output,
            "accommodation": accommodation_result.final_output,
            "optimized_plan": budget_result.final_output,
        }

    result = await supervisor()
    return result