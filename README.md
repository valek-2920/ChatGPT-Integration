# ChatGPT Integration

This project will allow you to consume the OpenAI API to use the software ChatGPT to build a Chatbot.

## To create the Python Virtual Environment

```bash
    pip3 install -U pip virtualenv
    py -m venv venv
```

To activate the virtual environment: .\venv\Scripts\activate
To deactivate the virtual environment: deactivate

## Packages used in Backend

```bash
    pip3 install openai==0.27.0
    python.exe -m pip install --upgrade pip
    pip3 install python-decouple==3.8 python-multipart==0.0.6 requests==2.28.2 fastapi==0.92.0
    pip3 install "uvicorn[standard]"
```

To run the API: uvicorn main:app --reload
To stop the API: CTRL + C

For the frontend, remember to install the needed npm packages using: npm install
To run the frontend: yarn start

## Acknowledgements

This project was inspired by the ChatGPT AI Voice Chatbot Build with React and FAST API Combo (https://udemy.com/course/chatgpt-ai-voice-chatbot-build-with-react-and-fast-api-combo) by Shaun McDonogh (https://udemy.com/user/shaun34/).
