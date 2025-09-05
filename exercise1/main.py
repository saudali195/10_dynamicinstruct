from agents import Agent, RunContextWrapper, Runner , trace
from pydantic import BaseModel
from connection import config
import asyncio , rich

# 1. define the context what the info will agent get.
class MedConsult(BaseModel):
    user_type = str
    complaint = str

# 2. Dynamic Instructions Function (will run at runTime)
async def med_instructions(ctx: RunContextWrapper[MedConsult], agent: Agent):
    #. ctx.context is the MedConsult instance you passed to Runner.run

    u = ctx.context.user_type.lower()
    
    if u == "patient":
        return(
            "Use very Simple Non-technical language to explain the medical condition and possible treatments. "
            "Be empathetic and reassuring in your responses. give clear next steps (Home, Care, )"
        )
    
    elif u == "medical Student":
        return (
            "Use Moderate Medical Terminology, but Define Terms. Provide teaching Points: Definitions, Pathophysiology, and Treatment Options."
            "Basic Pathophysiology, Suggested investigations and management. Encourage Learning resources."
    )

    elif u == "doctor":
        return(
            "Use Concise clinical Language and Accepted avbbreviations. Provide Differential Diagnoses, Suggested investigations and management plans."
            "investigations (labs/imaging), initial management, and escalation criteria."
        )

    else:
        return (
            "adapt your tone and detail level to the user's background."
        )

agent = Agent(
    name = "MedConsultAgent",
    instructions = med_instructions,
)

# 4) Run helper
async def main():
    # create an example context
    case = MedConsult(user_type="patient", complaint="I have a headache and fever for 2 days")
    with trace("Exercise 1 - Medical Consult"):
        result = await Runner.run(
            agent,
            f"My complaint: {case.complaint}",  # user prompt passed to the agent
            run_config=config,                  # from connection.py (model + client)
            context=case                        # the dynamic context that med_instructions will read
        )
        rich.print(result.final_output)        # show agent's reply

if __name__ == "__main__":
    asyncio.run(main())