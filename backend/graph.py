from typing import TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

from prompt import (
    CLARIFY_PROMPT,
    PLAN_PROMPT,
    RISK_PROMPT,
    TOOLS_PROMPT,
    MARKET_PROMPT,
)


class PlannerState(TypedDict):
    idea: str
    clarified_idea: str
    plan: str
    risks: str
    tools: str
    market_analysis: str
    memory_context: str

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3
)


def clarify_idea(state: PlannerState):
    prompt = PromptTemplate.from_template(CLARIFY_PROMPT)

    memory = state.get("memory_context", "")

    response = llm.invoke(
        prompt.format(
            idea=state["idea"],
            memory_context=memory
        )
    )

    return {"clarified_idea": response.content}


def create_plan(state: PlannerState):
    prompt = PromptTemplate.from_template(PLAN_PROMPT)
    response = llm.invoke(
        prompt.format(clarified_idea=state["clarified_idea"])
    )
    return {"plan": response.content}


def analyze_risks(state: PlannerState):
    prompt = PromptTemplate.from_template(RISK_PROMPT)
    response = llm.invoke(
        prompt.format(clarified_idea=state["clarified_idea"])
    )
    return {"risks": response.content}


def recommend_tools(state: PlannerState):
    prompt = PromptTemplate.from_template(TOOLS_PROMPT)
    response = llm.invoke(
        prompt.format(clarified_idea=state["clarified_idea"])
    )
    return {"tools": response.content}

def market_analysis(state: PlannerState):
    prompt = PromptTemplate.from_template(MARKET_PROMPT)
    response = llm.invoke(
        prompt.format(clarified_idea=state["clarified_idea"])
    )
    return {"market_analysis": response.content}


from langgraph.graph import StateGraph, START, END

def build_graph():
    graph = StateGraph(PlannerState)

    graph.add_node("clarify", clarify_idea)
    graph.add_node("plan", create_plan)
    graph.add_node("risks", analyze_risks)
    graph.add_node("tools", recommend_tools)
    graph.add_node("market", market_analysis)

    # Start with clarify
    graph.add_edge(START, "clarify")

    # Parallel branches after clarification
    graph.add_edge("clarify", "plan")
    graph.add_edge("clarify", "risks")
    graph.add_edge("clarify", "tools")
    graph.add_edge("clarify", "market")

    # All converge to END
    graph.add_edge("plan", END)
    graph.add_edge("risks", END)
    graph.add_edge("tools", END)
    graph.add_edge("market", END)

    return graph.compile()

