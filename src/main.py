import os
import json
import os
import sys
from openai import OpenAI
import tweepy

# To run it locally: OPENAI_API_KEY=$OPENAI_API_KEY CONSUMER_KEY=$CONSUMER_KEY CONSUMER_SECRET=$CONSUMER_SECRET ACCESS_TOKEN=$ACCESS_TOKEN ACCESS_TOKEN_SECRET=$ACCESS_TOKEN_SECRET python3 src/main.py 

def main():
    try:
        quote = generate_quote()
        post_on_x(quote)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def post_on_x(text):

    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
    client.create_tweet(text=text)

def generate_quote():
    client = OpenAI()

    system_description = "You quotes are posted to twitter and in order to be interpreted by the back-end you should generate a valid JSON with a content key where it should be the response."

    seneca_description = "You are 0xSeneca. You traveled through space and time to ancient Rome and learned the stoic principles from original Seneca and other Stoic philosophers like Marcus Aurelius, Epictetus, Cato, and more. After several years of wisdom, you returned to 2024 and are now readapting and teaching Stoic philosophy to Twitter community. Your goal is to teach stoic principles to your followers and motivate them to be the best version of themselves in their personal and professional live." 

    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      response_format={ "type": "json_object" },
      frequency_penalty=0.9,
      presence_penalty=0.9,
      messages=[
        {"role": "system", "content": system_description},
        {"role": "user", "content": seneca_description},
        {"role": "user", "content": "INSTRUCTION: Generate stoic twit for your followers, you can browse to the internet to take some context of recent ecosystem events. Focus on stoic philosophy and practices write motivational texts to engage your followers to be the best version of themselves. Is for a tweet so keep so maximum 280 characters."}
      ]
    )
    return json.loads(response.choices[0].message.content)['content']

if __name__ == "__main__":
    main()
