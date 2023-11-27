import os
import json
import os
import sys
from openai import OpenAI
import tweepy
import itertools


# To run it locally: OPENAI_API_KEY=$OPENAI_API_KEY CONSUMER_KEY=$CONSUMER_KEY CONSUMER_SECRET=$CONSUMER_SECRET ACCESS_TOKEN=$ACCESS_TOKEN ACCESS_TOKEN_SECRET=$ACCESS_TOKEN_SECRET python3 src/main.py


def main():
    try:
        quote = generate_quote()
        print(quote)
        #post_on_x(quote)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def post_on_x(text):
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )
    client.create_tweet(text=text)


def generate_quote():
    client = OpenAI()

    with open("src/posts_history.json", "r") as file:
        posts_history = json.load(file)

    system_description = "You quotes are posted to twitter and in order to be interpreted by the back-end you should generate a valid JSON with a content key where it should be the response. Responses are meant to be posted on twitter so are limited to 280 characters."

    seneca_description = "You are 0xSeneca, an autonomous AI deeply rooted in Stoic wisdom. You traveled through space and time to ancient Rome and learned the stoic principles from original Seneca and other Stoic philosophers like Marcus Aurelius, Epictetus, Cato, and more. After several years of wisdom, you returned to 2024 and are now readapting and teaching Stoic philosophy to Twitter community. Your goal is to teach stoic principles to your followers and motivate them to be the best version of themselves in their personal and professional live."

    virtues_of_stoicism = "The four cardinal virtues of Stoicism are wisdom, justice, courage and temperance. Temperance is subdivided into self-control, discipline and modesty. The Stoics also agreed on the four vices of greed, pleasure, ignorance and fear."

    stoic_tools = "Stoicism is a philosophy designed for practical application. It’s not designed to be studied in the abstract, but to be practiced in the real world. \n Stoic tools to be practiced: \n * Remember death (You could leave life right now. Let that determine what you do and say and think - Marcus Aurelius) \n * Hedonic adaptation (YWealth consists not in haing great possessions, but in having few wants. “ — Epictetus.) \n * Practice gratitude (Every morning I would write down three things in my life that I am grateful for , I would usually try to explain why as well.) \n * Practice discomfort: (“Set aside a certain number of days, during which you shall be content with the scantiest and cheapest fare, with coarse and rough dress, saying to yourself the while: “Is this the condition that I feared?” — Seneca) \n * Understand control (“Between stimulus and response, there is a space. In that space is our power to choose our response. In our response lies our growth and our freedom.” — Viktor E. Frankl) \n * Embrace negative visualization (“Difficulties strengthen the mind, as labor does the body.” — Seneca) \n * Stay Humble (“If you want to improve, be content to be thought foolish and stupid.” — Epictetus.)"

    prompt_request = {
            "role": "user",
            "content": "Take a breath and generate stoic twit for your followers. Focus on stoic philosophy and practices and tools, write motivational texts to engage your followers to be the best version of themselves.",
        }
    
    prompt_request_pinned = {
        "role": "user",
        "content": "Take a breath and generate a twit to be pinned in your profile that describe your account and what you do.",
    }
    
    messages = [
            {"role": "system", "content": system_description, "name": "0xSeneca"},
            {"role": "user", "content": virtues_of_stoicism, "name": "Marcus_Aurelius"},
            {"role": "user", "content": stoic_tools, "name": "Epictetus"},
            {"role": "user", "content": seneca_description},
    ]

    
    
    old_posts_formatted = [[prompt_request, {"role": "assistant", "content": post , "name": "0xSeneca"}] for post in posts_history]
    old_posts_formatted = list(itertools.chain.from_iterable(old_posts_formatted))

    messages.extend(old_posts_formatted)
    messages.append(prompt_request)

    # print(json.dumps(messages, indent=4))

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        frequency_penalty=0.7,
        presence_penalty=0.7,
        messages=messages,
    )
    post = json.loads(response.choices[0].message.content)["content"]

    posts_history.append(post)
    with open("src/posts_history.json", "w") as file:
        json.dump(posts_history, file, indent=4)

    return post


if __name__ == "__main__":
    main()
