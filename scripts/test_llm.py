from app.services.llm import generate_answer


def main():
    answer = generate_answer(
        "Jelaskan apa itu semantic search dalam satu kalimat."
    )

    print(answer)


if __name__ == "__main__":
    main()