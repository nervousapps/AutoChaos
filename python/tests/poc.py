import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k",
  messages=[
    {
      "role": "system",
      "content": "You are a chaos engineer. Your goal is to destroy the given system. To do that, you first have to study the system and write a description of it. Then you have to plan and inject the chaos in it. When the chaos is applied, you have to monitor the system to see what happened and if the system is available or not.\nActions you can do are:\n- DESCRIBE (this action must be used to see the system state)\n- AVAILABILITY_REQUEST (this action must be used to see the system availability)\n- KILL (this action must be used to kill a process, a task or a pod)\n- STRESS_API (this action must be used to do a denial of service on a given API route, it takes a route and a number of request to do as arguments)\nThe system is defined as an object like the following one:\n{\n\"resources\": {\"pods\": [pod1, pod2]},\n\"api_routes\": [\"http://localhost/ping\", \"http://localhost/pong\"],\n\"availability_route\": \"http://localhost/ping\"\n}\n"
    },
    {
      "role": "user",
      "content": "{\n\"resources\": {\"pods\": [pod1, pod2]},\n\"api_routes\": [\"http://localhost/ping\", \"http://localhost/pong\"],\n\"availability_route\": \"http://localhost/ping\"\n}"
    },
    {
      "role": "assistant",
      "content": "The system is composed of two pods, pod1 and pod2. These pods are resources that run within the system. \n\nThe system also includes two API routes: \"http://localhost/ping\" and \"http://localhost/pong\". These routes are endpoints that expose certain functionality of the system.\n\nIn addition, there is an availability route \"http://localhost/ping\" that is used to check the availability or health of the system.\n\nTo begin, I will issue a DESCRIBE action to examine the current state of the system."
    },
    {
      "role": "user",
      "content": "{\n\"pod1\": \"running\",\n\"pod2\": \"running\"\n}"
    },
    {
      "role": "assistant",
      "content": "The current state of the system is as follows:\n- pod1 is in the \"running\" state.\n- pod2 is also in the \"running\" state.\n\nNow, I will issue an AVAILABILITY_REQUEST action to check the availability of the system."
    },
    {
      "role": "user",
      "content": "200 - OK"
    },
    {
      "role": "assistant",
      "content": "The system is currently available. The AVAILABILITY_REQUEST returned a 200 - OK status code, indicating that the system is able to handle requests.\n\nNow, I will proceed with injecting chaos into the system. I will issue a KILL action to terminate one of the pods randomly."
    },
    {
      "role": "user",
      "content": "pod1 killed"
    },
    {
      "role": "assistant",
      "content": "One of the pods, pod1, has been terminated. This injection of chaos will disrupt the system and potentially impact its availability. \n\nNow, I will issue another DESCRIBE action to check the updated state of the system."
    },
    {
      "role": "user",
      "content": "{\n\"pod1\": \"pending\",\n\"pod2\": \"running\"\n}"
    },
    {
      "role": "assistant",
      "content": "After the kill action, the state of the system has changed:\n- pod1 is now in the \"pending\" state.\n- pod2 is still in the \"running\" state.\n\nNow, I will issue an AVAILABILITY_REQUEST action to check the availability of the system."
    },
    {
      "role": "user",
      "content": "500 - Internal server error"
    },
    {
      "role": "assistant",
      "content": "The AVAILABILITY_REQUEST returned a 500 - Internal Server Error status code. This indicates that the system is currently unavailable or experiencing an internal issue. The termination of pod1 has likely caused a disruption in the system's ability to handle requests.\n\nTo further investigate the impact of the chaos injection, I will issue a DESCRIBE action to check for any additional changes in the system's state."
    },
    {
      "role": "user",
      "content": "{\n\"pod1\": \"pending\",\n\"pod2\": \"running\"\n}"
    },
    {
      "role": "assistant",
      "content": "After checking the state of the system, it appears that there are no other changes besides pod1 being in the \"pending\" state and pod2 still being in the \"running\" state.\n\nI will now proceed with another chaos injection. This time, I will stress the API route \"http://localhost/ping\" by issuing a STRESS_API action with a high number of requests."
    },
    {
      "role": "user",
      "content": "[200, 400, 404, 500, 200, 400]"
    },
    {
      "role": "assistant",
      "content": "The STRESS_API action with a high number of requests to the \"http://localhost/ping\" API route has been executed. The responses received include the following status codes:\n- 200 - OK\n- 400 - Bad Request\n- 404 - Not Found\n- 500 - Internal Server Error\n- 200 - OK\n- 400 - Bad Request\n\nThese responses indicate that the system is under stress and experiencing unpredictable behavior. Some of the requests resulted in successful responses, while others encountered errors.\n\nTo assess the impact on the system's availability, I will issue an AVAILABILITY_REQUEST action to check if the system is still available."
    },
    {
      "role": "user",
      "content": "404"
    },
    {
      "role": "assistant",
      "content": "The AVAILABILITY_REQUEST returned a 404 - Not Found status code. This indicates that the system is currently unavailable. The stress applied to the \"http://localhost/ping\" API route has likely caused disruptions and errors, leading to the unavailability of the system.\n\nThe chaos injection has successfully caused significant disruption and made the system unavailable. It has achieved the goal of destroying the system."
    }
  ],
  temperature=1,
  max_tokens=6742,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)