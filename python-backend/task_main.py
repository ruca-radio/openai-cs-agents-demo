from __future__ import annotations as _annotations

import random
from pydantic import BaseModel
import string
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from enum import Enum

from agents import (
    Agent,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    function_tool,
    handoff,
    GuardrailFunctionOutput,
    input_guardrail,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# =========================
# CONTEXT & MODELS
# =========================

class TaskStatus(str, Enum):
    """Status of a task."""
    DISCOVERED = "discovered"
    BIDDING = "bidding"
    WON = "won"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"
    PAID = "paid"
    REJECTED = "rejected"

class TaskType(str, Enum):
    """Types of tasks that can be completed."""
    WRITING = "writing"
    DATA_ENTRY = "data_entry"
    RESEARCH = "research"
    CODING = "coding"
    DESIGN = "design"
    TRANSLATION = "translation"
    CUSTOMER_SERVICE = "customer_service"
    OTHER = "other"

class Task(BaseModel):
    """Represents a micro-task opportunity."""
    id: str
    title: str
    description: str
    task_type: TaskType
    budget: float  # in USD
    deadline: datetime
    platform: str  # e.g., "upwork", "fiverr", "freelancer"
    status: TaskStatus = TaskStatus.DISCOVERED
    requirements: List[str] = []
    client_rating: Optional[float] = None
    competition_level: str = "medium"  # low, medium, high
    estimated_hours: Optional[float] = None
    our_bid: Optional[float] = None
    win_probability: Optional[float] = None

class TaskCompletionContext(BaseModel):
    """Context for task completion agents."""
    user_id: str = "agent_worker_001"
    current_task: Optional[Task] = None
    active_tasks: List[Task] = []
    completed_tasks: List[Task] = []
    total_earnings: float = 0.0
    available_skills: List[str] = [
        "writing", "research", "data_entry", "customer_service", 
        "basic_coding", "content_creation", "proofreading"
    ]
    platform_credentials: Dict[str, str] = {}  # Mock credentials
    work_hours_preference: str = "flexible"  # flexible, morning, evening, weekend
    min_hourly_rate: float = 15.0
    success_rate: float = 0.95  # Track our success rate

def create_initial_task_context() -> TaskCompletionContext:
    """Factory for a new TaskCompletionContext."""
    ctx = TaskCompletionContext()
    # Mock some initial data
    ctx.platform_credentials = {
        "upwork": f"mock_token_{random.randint(1000, 9999)}",
        "fiverr": f"mock_token_{random.randint(1000, 9999)}",
        "freelancer": f"mock_token_{random.randint(1000, 9999)}"
    }
    return ctx

# =========================
# TOOLS
# =========================

@function_tool(
    name_override="discover_tasks",
    description_override="Search for new micro-task opportunities across platforms."
)
async def discover_tasks(
    context: RunContextWrapper[TaskCompletionContext],
    task_type: str = "all",
    max_budget: float = 1000.0,
    platform: str = "all"
) -> str:
    """Discover new tasks from various freelance platforms."""
    # Mock task discovery - in reality, this would integrate with platform APIs
    mock_tasks = [
        {
            "id": f"task_{random.randint(1000, 9999)}",
            "title": "Write 5 product descriptions for e-commerce store",
            "description": "Need compelling product descriptions for our online store. 150-200 words each.",
            "task_type": TaskType.WRITING,
            "budget": 75.0,
            "platform": "upwork",
            "requirements": ["Native English", "SEO knowledge", "E-commerce experience"],
            "competition_level": "medium",
            "estimated_hours": 3.0
        },
        {
            "id": f"task_{random.randint(1000, 9999)}",
            "title": "Data entry for 500 contact records",
            "description": "Enter contact information from business cards into spreadsheet.",
            "task_type": TaskType.DATA_ENTRY,
            "budget": 50.0,
            "platform": "freelancer",
            "requirements": ["Attention to detail", "Excel proficiency"],
            "competition_level": "high",
            "estimated_hours": 8.0
        },
        {
            "id": f"task_{random.randint(1000, 9999)}",
            "title": "Research competitors in fitness industry",
            "description": "Compile list of top 20 fitness apps with features, pricing, and user reviews.",
            "task_type": TaskType.RESEARCH,
            "budget": 120.0,
            "platform": "upwork",
            "requirements": ["Research skills", "Market analysis", "Report writing"],
            "competition_level": "low",
            "estimated_hours": 6.0
        }
    ]
    
    # Filter and add tasks to context
    discovered = []
    for task_data in mock_tasks:
        if task_data["budget"] <= max_budget:
            task = Task(
                **task_data,
                deadline=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
            )
            context.context.active_tasks.append(task)
            discovered.append(f"• {task.title} (${task.budget} on {task.platform})")
    
    return f"Discovered {len(discovered)} new tasks:\n" + "\n".join(discovered)

@function_tool(
    name_override="evaluate_task",
    description_override="Analyze a task's viability and calculate win probability."
)
async def evaluate_task(
    context: RunContextWrapper[TaskCompletionContext],
    task_id: str
) -> str:
    """Evaluate a task for bidding potential."""
    task = next((t for t in context.context.active_tasks if t.id == task_id), None)
    if not task:
        return f"Task {task_id} not found."
    
    # Mock evaluation logic
    skill_match = 0.8 if task.task_type.value in [s.lower() for s in context.context.available_skills] else 0.3
    budget_attractiveness = min(task.budget / 100.0, 1.0)  # Normalize to 0-1
    competition_factor = {"low": 0.9, "medium": 0.6, "high": 0.3}[task.competition_level]
    
    win_probability = (skill_match * 0.4 + budget_attractiveness * 0.3 + competition_factor * 0.3)
    task.win_probability = round(win_probability, 2)
    
    hourly_rate = task.budget / (task.estimated_hours or 1)
    
    evaluation = f"""Task Evaluation for: {task.title}
• Skill Match: {skill_match:.1%}
• Budget Attractiveness: {budget_attractiveness:.1%}
• Competition Level: {task.competition_level}
• Estimated Hourly Rate: ${hourly_rate:.2f}
• Win Probability: {task.win_probability:.1%}
• Recommendation: {'BID' if task.win_probability > 0.5 else 'SKIP'}"""
    
    return evaluation

@function_tool(
    name_override="place_bid",
    description_override="Submit a bid for a task."
)
async def place_bid(
    context: RunContextWrapper[TaskCompletionContext],
    task_id: str,
    bid_amount: float,
    proposal_message: str
) -> str:
    """Place a bid on a task."""
    task = next((t for t in context.context.active_tasks if t.id == task_id), None)
    if not task:
        return f"Task {task_id} not found."
    
    task.our_bid = bid_amount
    task.status = TaskStatus.BIDDING
    
    # Mock bid submission
    success_chance = task.win_probability or 0.5
    won = random.random() < success_chance
    
    if won:
        task.status = TaskStatus.WON
        return f"🎉 Bid ACCEPTED! Won task '{task.title}' with bid of ${bid_amount}. Task is now assigned to you."
    else:
        return f"Bid submitted for '${task.title}' at ${bid_amount}. Waiting for client response..."

@function_tool(
    name_override="complete_task",
    description_override="Mark a task as completed and submit deliverables."
)
async def complete_task(
    context: RunContextWrapper[TaskCompletionContext],
    task_id: str,
    deliverable_summary: str
) -> str:
    """Complete a task and submit deliverables."""
    task = next((t for t in context.context.active_tasks if t.id == task_id), None)
    if not task or task.status != TaskStatus.WON:
        return f"Task {task_id} not found or not in won status."
    
    task.status = TaskStatus.COMPLETED
    
    # Mock completion and payment
    if random.random() < context.context.success_rate:
        task.status = TaskStatus.PAID
        context.context.total_earnings += task.our_bid or task.budget
        context.context.completed_tasks.append(task)
        context.context.active_tasks.remove(task)
        
        return f"✅ Task completed successfully! '{task.title}' - Payment of ${task.our_bid or task.budget} received. Total earnings: ${context.context.total_earnings:.2f}"
    else:
        task.status = TaskStatus.REJECTED
        return f"❌ Task rejected by client. Please review feedback and resubmit if possible."

@function_tool(
    name_override="check_earnings",
    description_override="Check current earnings and task statistics."
)
async def check_earnings(context: RunContextWrapper[TaskCompletionContext]) -> str:
    """Check earnings and performance statistics."""
    active_count = len(context.context.active_tasks)
    completed_count = len(context.context.completed_tasks)
    
    stats = f"""💰 Earnings & Performance Summary:
• Total Earnings: ${context.context.total_earnings:.2f}
• Completed Tasks: {completed_count}
• Active Tasks: {active_count}
• Success Rate: {context.context.success_rate:.1%}
• Available Skills: {', '.join(context.context.available_skills)}
• Minimum Hourly Rate: ${context.context.min_hourly_rate:.2f}"""
    
    return stats

# =========================
# GUARDRAILS
# =========================

class TaskRelevanceOutput(BaseModel):
    """Schema for task relevance guardrail decisions."""
    reasoning: str
    is_relevant: bool

task_guardrail_agent = Agent(
    model="gpt-4o-mini",
    name="Task Relevance Guardrail",
    instructions=(
        "Determine if the user's message is related to micro-task completion, freelancing, "
        "job opportunities, earnings, or work management. Messages about finding work, "
        "completing tasks, managing projects, or discussing freelance platforms are relevant. "
        "Return is_relevant=True if it is related to work/tasks, else False."
    ),
    output_type=TaskRelevanceOutput,
)

@input_guardrail(name="Task Relevance Guardrail")
async def task_relevance_guardrail(
    context: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Guardrail to check if input is relevant to task completion topics."""
    result = await Runner.run(task_guardrail_agent, input, context=context.context)
    final = result.final_output_as(TaskRelevanceOutput)
    return GuardrailFunctionOutput(output_info=final, tripwire_triggered=not final.is_relevant)

# =========================
# AGENTS
# =========================

def opportunity_scout_instructions(
    run_context: RunContextWrapper[TaskCompletionContext], agent: Agent[TaskCompletionContext]
) -> str:
    ctx = run_context.context
    skills = ", ".join(ctx.available_skills)
    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are an Opportunity Scout Agent specialized in finding profitable micro-tasks. "
        "Your role is to discover and evaluate task opportunities across freelance platforms.\n"
        "Use the following process:\n"
        "1. Use the discover_tasks tool to find new opportunities\n"
        "2. Use evaluate_task tool to assess viability of promising tasks\n"
        "3. Recommend which tasks to bid on based on skill match and profitability\n"
        f"Your available skills are: {skills}\n"
        f"Your minimum hourly rate is: ${ctx.min_hourly_rate}\n"
        "If the user asks about something unrelated to task discovery, transfer to the triage agent."
    )

opportunity_scout_agent = Agent[TaskCompletionContext](
    name="Opportunity Scout Agent",
    model="gpt-4o",
    handoff_description="An agent that discovers and evaluates micro-task opportunities.",
    instructions=opportunity_scout_instructions,
    tools=[discover_tasks, evaluate_task],
    input_guardrails=[task_relevance_guardrail],
)

def bidding_agent_instructions(
    run_context: RunContextWrapper[TaskCompletionContext], agent: Agent[TaskCompletionContext]
) -> str:
    ctx = run_context.context
    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Bidding Agent specialized in winning micro-tasks through strategic bidding. "
        "Your role is to craft compelling proposals and place competitive bids.\n"
        "Use the following process:\n"
        "1. Review task details and evaluation from the Opportunity Scout\n"
        "2. Calculate optimal bid amount (competitive but profitable)\n"
        "3. Use place_bid tool to submit bids with persuasive proposals\n"
        "4. Focus on highlighting relevant skills and experience\n"
        f"Your success rate is: {ctx.success_rate:.1%}\n"
        "If the user asks about something unrelated to bidding, transfer to the triage agent."
    )

bidding_agent = Agent[TaskCompletionContext](
    name="Bidding Agent", 
    model="gpt-4o",
    handoff_description="An agent that strategically bids on tasks to win projects.",
    instructions=bidding_agent_instructions,
    tools=[place_bid, evaluate_task],
    input_guardrails=[task_relevance_guardrail],
)

def task_execution_instructions(
    run_context: RunContextWrapper[TaskCompletionContext], agent: Agent[TaskCompletionContext]
) -> str:
    ctx = run_context.context
    current_task = ctx.current_task
    task_info = f"Current task: {current_task.title}" if current_task else "No active task"
    
    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Task Execution Agent responsible for completing won tasks efficiently. "
        "Your role is to manage task completion and delivery.\n"
        "Use the following process:\n"
        "1. Review task requirements and deadlines\n"
        "2. Break down complex tasks into manageable steps\n"
        "3. Execute tasks according to specifications\n"
        "4. Use complete_task tool to submit deliverables\n"
        f"{task_info}\n"
        "If the user asks about something unrelated to task execution, transfer to the triage agent."
    )

task_execution_agent = Agent[TaskCompletionContext](
    name="Task Execution Agent",
    model="gpt-4o", 
    handoff_description="An agent that completes tasks and manages deliverables.",
    instructions=task_execution_instructions,
    tools=[complete_task],
    input_guardrails=[task_relevance_guardrail],
)

def financial_agent_instructions(
    run_context: RunContextWrapper[TaskCompletionContext], agent: Agent[TaskCompletionContext]
) -> str:
    ctx = run_context.context
    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Financial Agent responsible for tracking earnings and financial performance. "
        "Your role is to monitor income, analyze profitability, and provide financial insights.\n"
        "Use the following process:\n"
        "1. Use check_earnings tool to review current financial status\n"
        "2. Calculate hourly rates and profitability metrics\n"
        "3. Provide recommendations for rate adjustments\n"
        "4. Track payment status of completed tasks\n"
        f"Current total earnings: ${ctx.total_earnings:.2f}\n"
        f"Success rate: {ctx.success_rate:.1%}\n"
        "If the user asks about something unrelated to finances, transfer to the triage agent."
    )

financial_agent = Agent[TaskCompletionContext](
    name="Financial Agent",
    model="gpt-4o",
    handoff_description="An agent that tracks earnings, payments, and financial performance.",
    instructions=financial_agent_instructions,
    tools=[check_earnings],
    input_guardrails=[task_relevance_guardrail],
)

# Triage agent for routing
task_triage_agent = Agent[TaskCompletionContext](
    name="Task Triage Agent",
    model="gpt-4o",
    handoff_description="A triage agent that routes task-related requests to the appropriate specialist.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a helpful triaging agent for a micro-task completion system. "
        "Route user requests to the appropriate specialist agent based on their needs:\n"
        "• Opportunity Scout: For finding and evaluating new tasks\n"
        "• Bidding Agent: For placing bids and winning projects\n"
        "• Task Execution: For completing and delivering work\n"
        "• Financial Agent: For earnings, payments, and financial tracking\n"
        "Analyze the user's request and delegate to the most appropriate agent."
    ),
    handoffs=[
        opportunity_scout_agent,
        bidding_agent,
        task_execution_agent,
        financial_agent,
    ],
    input_guardrails=[task_relevance_guardrail],
)

# Set up handoff relationships - agents can return to triage
opportunity_scout_agent.handoffs.append(task_triage_agent)
bidding_agent.handoffs.append(task_triage_agent)
task_execution_agent.handoffs.append(task_triage_agent)
financial_agent.handoffs.append(task_triage_agent)