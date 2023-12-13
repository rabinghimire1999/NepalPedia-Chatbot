import openai
import pinecone
import streamlit as st
from sentence_transformers import SentenceTransformer

openai.api_key = "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"
model = SentenceTransformer('all-MiniLM-L6-v2')

# connection to pinecone
pinecone.init(      
	api_key='45b3f5d7-d358-4f02-bc8b-051cca14ec0a',      
	environment='gcp-starter'      
)      
index = pinecone.Index('qa-chatbot')
 
def find_match(input):
    """
    Finds the most relevant matches based on the encoded input.

    Parameters:
    input (str): The input text to be encoded and used for querying.

    Returns:
    str: A concatenated string of the top two matching texts retrieved from the index.
         The returned string contains the text of the best match followed by the text of the second-best match.
    """
    # The function takes an input string, encodes it using a pre-trained model, queries an index for similar items,
    # and returns a formatted string containing the texts of the top two matches retrieved.
    input_em = model.encode(input).tolist()  # Encodes the input text
    result = index.query(input_em, top_k=2, includeMetadata=True)  # Queries for the top 2 matches
    # Constructs a string containing the texts of the two best matches
    return result['matches'][0]['metadata']['text'] + "\n" + result['matches'][1]['metadata']['text']


def query_refiner(conversation, query):
    """
    Refines a user query by generating a more relevant question given the conversation context and initial query.

    Parameters:
    conversation (str): The conversation log or context to refine the query.
    query (str): The user's initial query to be refined based on the conversation context.

    Returns:
    str: A refined question that aims to be the most relevant to provide the user with an answer from a knowledge base.
    """
    # The function utilizes OpenAI's Completion API to refine the user's query by generating a question
    # that is contextually relevant to the provided conversation and the initial query.
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Extracts and returns the refined question from the OpenAI response
    return response['choices'][0]['text']


def get_conversation_string():
    """
    Generates a formatted conversation string from the stored session responses.

    Returns:
    str: A formatted string representing a conversation log between a human and a bot, 
         constructed from the stored session responses.
    """
    # The function iterates through stored 'requests' and 'responses' in the session state,
    # creating a formatted string that simulates a conversation between a human and a bot.
    conversation_string = ""
    for i in range(len(st.session_state['responses']) - 1):
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: " + st.session_state['responses'][i + 1] + "\n"
    
    return conversation_string


