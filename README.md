this was a project created entirely by Devin the AI SWE from Cognition Labs

I didn't do anything besides prompting it

Set Up the Frontend:

Open a terminal and navigate to the frontend directory.
Install the necessary dependencies by running:
npm install
or
yarn install
Start the development server by running:
npm start
or
yarn start
The frontend should now be running locally at http://localhost:3000.
Set Up the Backend:

Open another terminal and navigate to the root directory of the project (where the backend.py file is located).
Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate
Install the necessary dependencies by running:
pip install -r requirements.txt
Set the OpenAI API key as an environment variable:
export OPENAI_API_KEY=your_openai_api_key
Start the Flask backend server by running:
flask run
The backend should now be running locally at http://localhost:5000.
Update Frontend to Point to Local Backend:

Open the frontend/src/App.js file and update the backend URL to point to the local backend:
const backendUrl = "http://localhost:5000/analyze";
Test the Application:

With both the frontend and backend running locally, you can now test the application by navigating to http://localhost:3000 in your browser and uploading a lease document or inputting lease text for analysis.
