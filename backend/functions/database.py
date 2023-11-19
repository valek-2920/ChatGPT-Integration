import json
import random


def get_recent_messages():
    file_name = "stored_data.json"

    # Define instructions
    learn_instruction = {
        "role": "system",
        "content": "You are interviewing the user for a job as a retail assistant. Ask short questions that are relevant to the junior position. Your name is Glenda. The user is callend Jimmy. Keep your answers to under 25 words"
    }

    # Init messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + \
            " Your response will include some dry humour."
    else:
        learn_instruction["content"] = learn_instruction["content"] + \
            " Your response will include a rather challenging question."

    messages.append(learn_instruction)

    # get last 5 messages of data
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass

    return messages


def store_messages(request_message, response_message):
    file_name = "stored_data.json"

    # Excluded first message
    messages = get_recent_messages[1:]

    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}

    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)


def reset_messages():
    open("stored_data.json", "w")