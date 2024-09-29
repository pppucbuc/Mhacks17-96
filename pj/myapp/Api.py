import time
from openai import OpenAI

# Enter your Assistant ID here.
def gpt_request(data, expect):

    # Create a thread with a message, put this in the route that handle the form submission on the website 
    Message = f"The student is expect to get an {expect}. encourage the student if his expectation is higher than the prediction and tell the student the area(quiz, assignment, exam, project, participation) they should improve.Praise the student if his expectation is the same or lower than the prediction. Here is the prediction:{data}"       # to do
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # Update this with the query you want to use.
                "content": Message,
            }
        ]
    )

    # Submit the thread to the assistant (s a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f"👉 Run Created: {run.id}")

    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"🏃 Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f"🏁 Run Completed!")

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    # Print the latest message.
    latest_message = messages[0]
    print(f"💬 Response: {latest_message.content[0].text.value}")
    return latest_message.content[0].text.value