from vendi_sdk import Vendi
import openai

from vendi_sdk.runtime.instrument import get_context

project_id = "<project_id>"

vendi = Vendi(
    api_key="<vendi_api_key>",
    project_id=project_id,
)

vendi.instrument(
    disable_batch=True,
    tags={"country": "USA", "new_property": "new_value"}
)

openai.api_key = "<openai-api-key>"


@vendi.workflow(workflow_name="casual-chat")
def empty_task():
    get_context().set_run_id("1119")
    openai.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot.",
            },
            {
                "role": "user",
                "content": "Whats is your favourite color?",
            },
        ],
    )


empty_task()

# vendi.runtime.feedback(
#     workflow_name="chat-2",
#     run_id="1235",
#     value={"new_status_1": "matan"},
# )
#
