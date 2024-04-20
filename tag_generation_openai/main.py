import os
from openai import OpenAI
from dotenv import load_dotenv
import re
import json

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_response(prompt_dict):
    # Assume `instruction` is a well-defined string as in your script above.
    prompt = create_prompt_to_generate_reply(prompt_dict)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        response_dict = parse_api_response(reply.strip())
        print(reply)
        print(response_dict)
        return response_dict
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # or handle it in some other appropriate way

def convert_keywords_to_array(keywords_string):
    # Split the string by new line character and ignore the first element
    # as it contains "Keywords/Categories:"
    keywords_list = keywords_string.split("\n")[1:]
    
    # Remove the numbering and leading/trailing whitespaces
    keywords_array = [keyword.split(".")[1].strip() for keyword in keywords_list]
    
    return keywords_array


def create_prompt_to_generate_reply(prompt_dict):
    # Assuming the keys exist in prompt_dict, construct the prompt string
    return f"Title: \"{prompt_dict['title']}\", Content: \"{prompt_dict['content']}\", Username: \"{prompt_dict['username']}\", Number of Comments: \"{prompt_dict['comments']}\"', Upvotes: \"{prompt_dict['upvotes']}\"', Created At: \"{prompt_dict['created_utc']}\""

instruction = """
After identifying if a Reddit post is trending and relevant based on themes of personal growth or challenges:

1. Generate a human-like and natural-sounding title for a reply, containing 2-4 words, that resonates with the post's theme.

2. Create a content (text/paragraph) related to the post's content and the generated title. The content should be 20-30 words long and reflect general support, insight, or humor relevant to personal growth. Avoid direct or specific references to individual situations.

3. Suggest a background color based on the theme of the content and title of the post, which seems attractive and soothing. Along with the background color, suggest a text color which goes with the contrast of the background color for good readability.

4. Compose a quote that encapsulates the essence or moral of the content piece. This quote should be thoughtful and relevant to the themes discussed in the post and the generated title. The quote should 10-12 words long.

5. To a Reddit post titled "[title]", which delves into "[content]", generate a reply addressing the general theme of personal challenges and growth with empathy and understanding. The response should be casual, friendly, and no longer than 3-4 sentences, making it feel like a natural extension of a Reddit conversation. Use common, accessible language and maintain a supportive tone. For example, instead of directly suggesting therapy, say, 'I  took a lot from this advice, perhaps you will too. - [LINK_FOR_THE_CONTENT].' Ensure the linked material [LINK_FOR_THE_CONTENT] only contains general piece of advice or insights, that was generated in the above points, providing a relatable or humorous perspective that could be helpful. This can be at the end of the reply, which starts with a general response to the user's concern.

Give the response in the following format as a python dictionary (in which the keys and values are strings) : "title: [Response of 1], content: [Response of 2], bg_color: [HEX Code of Response 3's background color], color: [HEX Code of Response 3's text color], quote: [Response of 4], reply: [Response of 5]"
"""


def parse_api_response(input_data):
    try:
        # First, attempt to parse the input as JSON
        parsed_dict = json.loads(input_data)
    except json.JSONDecodeError:
        # If JSON parsing fails, fall back to regex parsing for the plain text format
        # Define a regular expression pattern to handle both quoted and unquoted values
        pattern = r'(\w+):\s*(?:"([^"]*)"|([^,\n]*))'
        
        # Use findall function to extract all key-value pairs from the string
        matches = re.findall(pattern, input_data)

        # Initialize an empty dictionary to store key-value pairs
        parsed_dict = {}

        # Iterate over each match and add it to the dictionary
        for match in matches:
            key, value1, value2 = match
            parsed_dict[key] = value1 if value1 else value2.strip()

    return parsed_dict
