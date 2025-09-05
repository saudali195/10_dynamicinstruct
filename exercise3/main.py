# main.py
import asyncio
import rich
from pydantic import BaseModel
from agents import Agent, RunContextWrapper, Runner, trace
from connection import config

# 1) Context model
class TravelContext(BaseModel):
    trip_type: str          # "adventure" | "cultural" | "business"
    traveler_profile: str   # "solo" | "family" | "executive"
    extra_notes: str = ""   # optional

# 2) Dynamic instructions
async def travel_instructions(ctx: RunContextWrapper[TravelContext], agent: Agent):
    trip = (ctx.context.trip_type or "").strip().lower()
    profile = (ctx.context.traveler_profile or "").strip().lower()
    notes = ctx.context.extra_notes or ""

    # Adventure + Solo
    if trip == "adventure" and profile == "solo":
        return (
            "You are a travel planning assistant for an ADVENTURE SOLO traveler. "
            "Suggest thrilling activities (hiking, rafting, paragliding), focus on safety tips (gear, guides, insurance), "
            "and recommend budget-friendly social hostels or group tours for meeting other travelers. "
            + (f"Notes: {notes}" if notes else "")
        )

    # Cultural + Family
    if trip == "cultural" and profile == "family":
        return (
            "You are a travel planner for a FAMILY interested in CULTURAL exploration. "
            "Recommend educational attractions, kid-friendly museums, interactive experiences, guided city tours, "
            "and family accommodations with amenities (family rooms, child-friendly meals). "
            + (f"Notes: {notes}" if notes else "")
        )

    # Business + Executive
    if trip == "business" and profile == "executive":
        return (
            "You are a travel assistant for an EXECUTIVE on a BUSINESS trip. "
            "Focus on efficiency: hotels near airports or business districts, reliable Wi-Fi, business centers, "
            "airport transfers, premium lounges, and time-saving itineraries. "
            + (f"Notes: {notes}" if notes else "")
        )

    # Fallback for other combinations
    return (
        f"You are a travel planner. The traveler is {profile} on a {trip} trip. "
        "Provide balanced recommendations that mix comfort, value, and experiences. "
        + (f"Notes: {notes}" if notes else "")
    )

# 3) Create the Agent
travel_agent = Agent(
    name="TravelPlanningAgent",
    instructions=travel_instructions,
)

# 4) Runner example
async def main():
    case1 = TravelContext(trip_type="adventure", traveler_profile="solo", extra_notes="Wants hiking in safe areas")
    case2 = TravelContext(trip_type="cultural", traveler_profile="family", extra_notes="Kids are 6 and 10 years old")
    case3 = TravelContext(trip_type="business", traveler_profile="executive")
    case4 = TravelContext(trip_type="adventure", traveler_profile="family")

    for idx, case in enumerate([case1, case2, case3, case4], start=1):
        with trace(f"Exercise 3 - Travel Example {idx}"):
            prompt = f"Plan my trip. Context: trip={case.trip_type}, profile={case.traveler_profile}."
            result = await Runner.run(
                travel_agent,
                prompt,
                run_config=config,
                context=case
            )
            print("\n" + "="*36)
            rich.print(f"Example {idx} - Context: {case.json()}")
            rich.print("Agent reply:")
            rich.print(result.final_output)
            print("="*36 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
