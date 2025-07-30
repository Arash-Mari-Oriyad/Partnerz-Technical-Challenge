# app.py

from qa_agent import answer_question

def main():
    print("Welcome to the Intercom Help Center AI Agent!")
    while True:
        q = input("\nEnter your question (or 'exit' to quit): ")
        if q.strip().lower() == 'exit':
            break
        answer = answer_question(q)
        print("\n" + answer)

if __name__ == "__main__":
    main()
