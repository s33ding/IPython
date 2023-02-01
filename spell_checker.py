import sys
import requests

prompt = f"\033[34mlanguagetool.api 🤖 >>>\033[0m "

def menu(text):
    print("\033[31m0 - RETRY!\033[0m")
    print("Choose this option to recheck the text again")

    print("\033[32m1 - PROCEED\033[0m")
    print("Choose this option to replace the incorrect text with the suggested correction")

    print("\033[32m2 - Retype incorrect text\033[0m")
    print("Choose this option to manually type the correction before proceeding")

    menu_choice = int(input("Enter your choice: "))

    # Recursion
    if menu_choice == 0:
        return True

    # Replace the incorrect text with the correct text
    if menu_choice == 1:
        text = text[:start] + correct_text + text[end:]
        return text

    # Replace the incorrect text with the correct text
    if menu_choice == 2:
        print(f"\nRETYPE TO LEARN MORE:")
        print(f"\033[32m{text}\033[0m")
        trash =  input(f'{prompt}')
        print("\n=)\n")
        return text
    else:
        print("erro")

def check_grammar(text = input(f"{prompt}")):
    # Code for checking grammar here
    language = "en-US"

    if len(sys.argv) > 1 and sys.argv[1] == "1":
        language = "pt-BR"

    # Define the API endpoint
    endpoint = "https://languagetool.org/api/v2/check"

    # Define the API request parameters
    params = {
        "text": text,
        "language": language
    }

    # Make a request to the API
    response = requests.post(endpoint, data=params)

    # Check the status code of the response
    if response.status_code == 200:
        # Extract the corrections made by Language Tool
        corrections = response.json()["matches"]

        # Print the corrections
        for correction in corrections:
            incorrect_text = correction["message"]
            correct_text = correction["replacements"][0]["value"]
            start = correction["offset"]
            end = correction["offset"] + correction["length"]
            rule_id = correction["rule"]["id"]

            print(f"\033[32m{text[:start]}\033[0m\033[31m{text[start:end]}\033[0m\033[32m{text[end:]}\033[0m")
            print(f"Incorrect text: {incorrect_text}")
            print(f"Correct text: \033[32m{correct_text}\033[0m")
            print(f"Location: {start} - {end}")
            print(f"Rule ID: {rule_id}")
            print("\n")

        recursion = menu(text)
        print(recursion)

    else:
        # Print an error message
        print("An error occurred while checking the text.")

    if recursion  == True:
        text = input(f"{prompt}")
        check_grammar(text)

    print("\033[32mOK!\033[0m")

# Call the function to check the grammar of the given text
check_grammar()
