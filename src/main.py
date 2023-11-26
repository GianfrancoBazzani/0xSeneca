import os
import sys

# To run it locally: OPEN_AI_KEY=$OPEN_AI_KEY TWITTER_API_KEY=$TWITTER_API_KEY TWITTER_API_KEY_SECRET=$TWITTER_API_KEY_SECRET python3 src/main.py

def main():
    """Main function."""
    try:
        # Get report_folder_name environment var
        open_ai_key = os.getenv("OPEN_AI_KEY")
        twitter_api_key = os.getenv("TWITTER_API_KEY")
        twitter_api_key_secret = os.getenv("TWITTER_API_KEY_SECRET")

        if (open_ai_key and twitter_api_key and twitter_api_key_secret):
            print("OKOK")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
