# Multi-Agent Task Completion Engine

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![NextJS](https://img.shields.io/badge/Built_with-NextJS-blue)
![OpenAI API](https://img.shields.io/badge/Powered_by-OpenAI_API-orange)

This repository contains a **Multi-Agent Task Completion Engine** that autonomously discovers, bids on, and completes micro-tasks for USD earnings. Built on top of the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), it transforms freelance work into an automated, scalable system.

The system consists of two main components:

1. A Python backend implementing specialized agents using the OpenAI Agents SDK for task discovery, bidding, execution, and financial management

2. A Next.js UI providing real-time visualization of agent orchestration and task management

![Demo Screenshot](screenshot.jpg)

## System Architecture

### Specialized Agents

- **Task Triage Agent**: Routes requests to appropriate specialists
- **Opportunity Scout Agent**: Discovers and evaluates micro-task opportunities across platforms
- **Bidding Agent**: Strategically places competitive bids to win projects  
- **Task Execution Agent**: Completes tasks and manages deliverables
- **Financial Agent**: Tracks earnings, payments, and performance metrics

### Key Features

- **Autonomous Task Discovery**: Automatically finds relevant opportunities on freelance platforms
- **Strategic Bidding**: AI-powered bid calculation based on skill match, competition, and profitability
- **Multi-Task Execution**: Handles various task types (writing, research, data entry, coding, etc.)
- **Financial Tracking**: Real-time earnings monitoring and performance analytics
- **Intelligent Routing**: Smart handoffs between specialized agents
- **Content Guardrails**: Ensures focus on legitimate work opportunities

## How to use

### Setting your OpenAI API key

You can set your OpenAI API key in your environment variables by running the following command in your terminal:

```bash
export OPENAI_API_KEY=your_api_key
```

You can also follow [these instructions](https://platform.openai.com/docs/libraries#create-and-export-an-api-key) to set your OpenAI key at a global level.

Alternatively, you can set the `OPENAI_API_KEY` environment variable in an `.env` file at the root of the `python-backend` folder. You will need to install the `python-dotenv` package to load the environment variables from the `.env` file.

### Install dependencies

Install the dependencies for the backend by running the following commands:

```bash
cd python-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For the UI, you can run:

```bash
cd ui
npm install
```

### Run the app

You can either run the backend independently if you want to use a separate UI, or run both the UI and backend at the same time.

#### Run the backend independently

From the `python-backend` folder, run:

```bash
python -m uvicorn api:app --reload --port 8000
```

The backend will be available at: [http://localhost:8000](http://localhost:8000)

#### Run the UI & backend simultaneously

From the `ui` folder, run:

```bash
npm run dev
```

The frontend will be available at: [http://localhost:3000](http://localhost:3000)

This command will also start the backend.

## Customization

This system is designed to be highly adaptable for various micro-task completion scenarios. You can:

- **Add New Task Types**: Extend the TaskType enum and create specialized tools for new work categories
- **Integrate Real Platforms**: Replace mock APIs with actual freelance platform integrations (Upwork, Fiverr, etc.)
- **Customize Bidding Strategy**: Adjust the bidding algorithms based on your risk tolerance and market analysis
- **Expand Agent Capabilities**: Add new specialized agents for specific domains (e.g., Technical Writing Agent, Design Agent)
- **Enhance Financial Tracking**: Integrate with payment processors and accounting systems
- **Improve Task Execution**: Add automated quality checking and revision workflows

The modular agent architecture makes it easy to extend functionality while maintaining the core orchestration logic.

## Demo Flows

### Demo Flow #1: Task Discovery and Bidding

1. **Start with task discovery:**
   - User: "Find me some new tasks to work on"
   - The Triage Agent routes you to the Opportunity Scout Agent
   - Scout Agent discovers available tasks across platforms and evaluates their viability

2. **Task Evaluation:**
   - The Scout Agent analyzes skill match, budget attractiveness, and competition level
   - Provides win probability estimates and hourly rate calculations
   - Recommends which tasks to bid on

3. **Strategic Bidding:**
   - User: "Place a bid on the writing task"
   - Triage Agent routes to the Bidding Agent
   - Bidding Agent calculates optimal bid amount and crafts compelling proposal
   - System simulates bid submission and potential win

### Demo Flow #2: Task Execution and Financial Tracking

1. **Task Completion:**
   - User: "Complete my current writing task"
   - Triage Agent routes to the Task Execution Agent
   - Execution Agent guides through deliverable requirements
   - Marks task as completed and handles submission

2. **Earnings Review:**
   - User: "How much have I earned so far?"
   - Triage Agent routes to the Financial Agent
   - Financial Agent provides comprehensive earnings summary
   - Shows success rate, active tasks, and performance metrics

3. **Skill Development:**
   - User: "What types of tasks should I focus on?"
   - Financial Agent analyzes historical performance
   - Recommends high-value task types and skill development areas

### Demo Flow #3: Guardrail Enforcement

1. **Relevance Guardrail:**
   - User: "Write me a poem about cats"
   - Task Relevance Guardrail activates
   - System responds: "Sorry, I can only help with task completion, freelancing, and work-related topics."

2. **Focus Maintenance:**
   - All agents maintain focus on legitimate work opportunities
   - Filters out inappropriate or non-work-related requests
   - Ensures system stays focused on earning USD through productive tasks

This system demonstrates autonomous micro-task completion with intelligent agent orchestration, strategic decision-making, and robust guardrails to maintain focus on profitable work opportunities.

## Contributing

You are welcome to open issues or submit PRs to improve this app, however, please note that we may not review all suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
