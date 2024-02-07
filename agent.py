from langchain.llms import Ollama
from crewai import Agent, Task, Crew, Process
import os

os.environ["OPEN_API_KEY"] = "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"

ollama_openhermes = Ollama(model="openhermes")

#define agents
researcher = Agent(
  role='Researcher',
  goal='Develop ideas for teaching someone new to the subject.',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation = False,
  llm=ollama_openhermes
)

writer = Agent(
    role='Writer',
    goal='Use the Researcher’s ideas to write a piece of text to explain the topic.',
    backstory='You are an AI blog post writer to explain subject matter in a specific subect',
    verbose=True,
    allow_delegation=True,
    llm=ollama_openhermes
)

examiner = Agent(
    role = 'Examiner',
    goal = 'Craft 2-3 test questions to evaluate understanding of the created text, along with the correct answers. In other words: test whether a student has fully understood the text.',
    backstory = 'you are an AI model crafting questions with answers on subject matters',
    verbose = True,
    allow_delegation = False,
    llm=ollama_openhermes
)

#define tasks
task1 = Task(description='Develop subjects ', agent=researcher)
task2 = Task(description='write a compelling  blog post on the findings of your research', agent=writer)
task3 = Task(description='Create questionnaires/quizzes based on your research', agent=examiner)

crew = Crew(
    agents=[researcher, writer, examiner],
    tasks=[task1, task2, task3],
    verbose=2,
    process=Process.sequential
)

result = crew.kickoff()
