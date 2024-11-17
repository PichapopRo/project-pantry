"""The handler for the GPT model."""
from openai import OpenAI
from typing import Any
from decouple import config

client = OpenAI(api_key=config("OPENAI_APIKEY", default="Fake-API-key"))


class GPTHandler:
    """
    Handles the logic for the interaction with the OpenAI's GPT model.
    
    :param context: The context of the model.
    :param model: The GPT's model name.
    """

    def __init__(self, context: str, model: str) -> None:
        """
        Initialize the class.
        
        :param context: The context of the model.
        :param model: The GPT's model name.
        """
        self.context = context
        self.model = model
        
    def __get_message(self, input: str) -> list[dict[str, Any]]:
        """
        Generate the message dialog list.
        
        :return: The list  of multiple dictionaries containing the dialog.
        """
        return [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": self.context
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": input
                    }
                ]
            }
        ]
    
    def generate(self, input: str) -> str:
        """
        Generate a response from the model.
        
        :param input: The input to the model.
        :return: The response from the model.
        """
        response = client.chat.completions.create(
            model=self.model,
            messages=self.__get_message(input),
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )
        return response.choices[0].message.content
