import requests
import json
import html
import random

def fetch_questions(amount=5):
    """
    Fetches trivia questions from the Open Trivia Database API.
    """
    # API URL: asking for specific amount of multiple choice questions
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"

    try:
        print("Loading questions from the Trivia Database...")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data['results']
        else:
            print("Error fetching questions.")
            return []
            
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

def run_quiz():
    """
    Runs the main quiz loop.
    """
    questions = fetch_questions()
    
    if not questions:
        print("Could not start the quiz. Please try again later.")
        return

    score = 0
    total = len(questions)
    
    print(f"\nWelcome to the Quick Quiz! Answer {total} questions.\n")

    for index, item in enumerate(questions, 1):
        # The API returns text with HTML entities (like &quot;), so we decode them
        question_text = html.unescape(item['question'])
        correct_answer = html.unescape(item['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in item['incorrect_answers']]

        # Combine all answers and shuffle them so the correct one isn't always first
        all_options = incorrect_answers + [correct_answer]
        random.shuffle(all_options)

        print(f"Q{index}: {question_text}")
        
        # Display options labeled 1, 2, 3, 4
        for i, option in enumerate(all_options, 1):
            print(f"  {i}. {option}")

        # Get user input
        while True:
            try:
                choice = int(input("\nYour answer (enter the number): "))
                if 1 <= choice <= len(all_options):
                    selected_answer = all_options[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(all_options)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Check answer
        if selected_answer == correct_answer:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong. The correct answer was: {correct_answer}\n")

    # Final Score
    print("="*30)
    print(f"Quiz Finished! You got {score}/{total} correct.")
    print("="*30)

if __name__ == "__main__":
    run_quiz()