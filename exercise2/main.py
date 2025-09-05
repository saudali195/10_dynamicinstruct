# main.py
import asyncio
import rich
from pydantic import BaseModel
from agents import Agent, RunContextWrapper, Runner, trace
from connection import config

# -- 1) Define the context shape the agent will receive --
class SeatPrefContext(BaseModel):
    seat_preference: str   # expected: "window" | "aisle" | "middle" | "any"
    travel_experience: str # expected: "first_time" | "occasional" | "frequent" | "premium"
    extra_notes: str = ""  # optional notes (empty string by default)

# -- 2) The dynamic instruction function --
# This function is called by the SDK before the model is invoked.
# It receives a RunContextWrapper whose .context is a SeatPrefContext instance.
async def seat_pref_instructions(ctx: RunContextWrapper[SeatPrefContext], agent: Agent):
    seat = (ctx.context.seat_preference or "").strip().lower()
    exp = (ctx.context.travel_experience or "").strip().lower()
    notes = ctx.context.extra_notes or ""

    # Premium travelers get luxury-focused answers regardless of seat
    if exp == "premium":
        return (
            "You are an airline booking assistant speaking to a PREMIUM traveler. "
            "Highlight luxury options and benefits: upgrades, extra legroom, priority boarding, lounge access, "
            "and how to request them. Keep tone professional and concise. " + (f"Notes: {notes}" if notes else "")
        )

    # Window + First-time traveller
    if seat == "window" and exp == "first_time":
        return (
            "You are an airline booking assistant speaking to a FIRST-TIME flyer who prefers a WINDOW seat. "
            "Explain the benefits of a window seat in simple reassuring language: scenic views, a surface to lean on, "
            "fewer disturbances from aisle traffic. Provide calming tips for first flights (breathing, ear pressure tips), "
            "and briefly describe what to expect during takeoff and landing. Offer alternatives if the window is unavailable. "
            + (f"Notes: {notes}" if notes else "")
        )

    # Middle + Frequent traveller
    if seat == "middle" and exp == "frequent":
        return (
            "You are an airline booking assistant speaking to a FREQUENT flyer who is seated in the MIDDLE. "
            "Acknowledge this is a compromise. Offer pragmatic strategies: request a seat change at check-in, consider early boarding, "
            "pack light to fit carry-on carefully, be polite when asking neighbors for small favors. Suggest alternatives like paid seat selection "
            "or using loyalty status to improve seating. Keep it short and practical. " + (f"Notes: {notes}" if notes else "")
        )

    # Any + other experience levels
    if seat == "any":
        return (
            "You are an airline booking assistant. The passenger has no strong seat preference ('any'). "
            "Ask (briefly in your reply) about their top priorities (legroom, quick exit, scenic view, mobility needs). "
            "Then recommend the best seat match based on their priorities and mention upgrade options if relevant. "
            + (f"Notes: {notes}" if notes else "")
        )

    # Generic window advice (non-first-time)
    if seat == "window":
        return (
            "You are an airline booking assistant. Explain the pros and cons of a window seat (view, lean surface, less aisle disturbance) "
            "and provide practical tips for comfort on longer flights (stretching, position changes, choosing a spot near the wing vs. window row). "
            + (f"Notes: {notes}" if notes else "")
        )

    # Generic aisle advice
    if seat == "aisle":
        return (
            "You are an airline booking assistant. Explain the pros and cons of an aisle seat (easy access, more room to stretch) "
            "and mention polite ways to ask others to move, and stretch/exercise suggestions for long-haul travel. "
            + (f"Notes: {notes}" if notes else "")
        )

    # Generic middle (non-frequent)
    if seat == "middle":
        return (
            "You are an airline booking assistant. Describe middle-seat tradeoffs and give tips to make it more comfortable "
            "(request bulkhead/exit rows, use travel pillows, plan aisle access breaks). Offer alternatives/upgrade suggestions. "
            + (f"Notes: {notes}" if notes else "")
        )

    # Default fallback
    return (
        "You are an airline booking assistant. Provide balanced pros and cons for window/aisle/middle seats, "
        "ask a clarifying question about priorities if needed, and recommend upgrades or alternatives when useful. "
        + (f"Notes: {notes}" if notes else "")
    )

# -- 3) Create the Agent with dynamic instructions --
seat_agent = Agent(
    name="SeatPreferenceAgent",
    instructions=seat_pref_instructions,
)

# -- 4) Runner example to test the agent --
async def main():
    # Example 1: Window + First-time
    case1 = SeatPrefContext(seat_preference="window", travel_experience="first_time", extra_notes="Nervous about flying")
    # Example 2: Middle + Frequent
    case2 = SeatPrefContext(seat_preference="middle", travel_experience="frequent")
    # Example 3: Any + Occasional
    case3 = SeatPrefContext(seat_preference="any", travel_experience="occasional", extra_notes="Has knee problem")

    # Run each example sequentially
    for idx, case in enumerate([case1, case2, case3], start=1):
        with trace(f"Exercise 2 - SeatPref Example {idx}"):
            prompt = f"I need help choosing a seat. Context: seat={case.seat_preference}, experience={case.travel_experience}."
            result = await Runner.run(
                seat_agent,
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
