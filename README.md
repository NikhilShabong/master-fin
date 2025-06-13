Masters
This project is a full stack prototype for a conversational fitness coach. It combines a React front end for onboarding and chat with a FastAPI back end that calls OpenAI models to provide tailored advice and workout plans.
Features
•	Onboarding form to collect user traits (sleep, nutrition, mindset, etc.)
•	KPI selection to choose fitness goals and compute a future trait vector
•	Chat interface where users can ask questions and receive advice
•	Workout generator that produces a weekly plan based on user archetypes
•	Uses embeddings to classify user input and JSON files to store habit, tone and workout data
Repository Layout
Backend/   # FastAPI service and data files
Frontend/  # React app (Vite)
Important back end modules include router.py with the /generate_advice and /generate_workout routes and utilities such as advice_generator.py and workout_generator.py. The front end entry point is Frontend/App.jsx which handles routing between the onboarding form, KPI selection and chat components.
Setup
Back end
1.	Create a Python environment (Python 3.10+).
2.	Install dependencies:
pip install -r Backend/requirements.txt
3.	Set the environment variable OPENAI_API_KEY with your OpenAI key.
4.	Start the API:
5.	cd Backend
uvicorn main:app --reload
Front end
1.	Install Node.js (version matching the package.json).
2.	Install packages:
3.	cd Frontend
npm install
4.	Start the development server:
npm run dev
The React app will connect to the FastAPI server running on localhost:8000.
Data Files
Several JSON files in the Backend directory provide habit suggestions, tone strategies and workout tailoring parameters. User submissions are saved to Backend/responses.json with a timestamp and ID.
Notes
•	The project uses OpenAI's GPT models (see gpt_caller.py). Ensure API access before running.
•	The data files are examples and can be expanded to cover more KPIs or traits.
•	This code was made in the Cursor IDE, which utalises Claude and other LLMs to help with syntax and formatting
•	I will be constantly updating this code with better functionality!

