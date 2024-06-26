# Wikiquiz

Play quiz with a wikipedia page of any person. This project uses the wikipedia api to fetch articles and search on wikidata for structured information about the person.
This structured information is passed to a LLM (here chatgtp turbo 3.5) to generate a question and fake answers. Questions are stored in a MongoDB to avoid prompting the AI to often.

For now this project only works for the german language. For other languages you need to modify the prompts.

This Repository only contains the backend service - for the frontend visit https://github.com/mjiruobe/Wikiquiz-Android



https://github.com/mjiruobe/Wikiquiz/assets/68758914/6efb457f-1304-41e9-9b5d-d8f9fa701b16



## How to run

- Install _docker_ and _git_ if not done yet.
- Execute the command: `git clone https://github.com/mjiruobe/Wikiquiz`
- Execute: `cd Wikiquiz`
- Enter a Open AI API Key in .env.example file and rename it to .env, also put a API Key in this file to secure your Wikiquiz Instance from unauthorized access. Also give the Mongo DB a username and password for making it more secure.
- Execute: `docker compose up`
- Follow the instructions of https://github.com/mjiruobe/Wikiquiz-Android to create an Flutter (Android client) for this Wikiquiz backend.

## Disclamer

This project is not production ready. It is a proof of concept.
I don't recommend to make this project public available outside of your network without any modification e.g. an nginx tranmisson proxy for encrypted traffic to the API.
