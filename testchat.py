from chat import chat
import argparse
import asyncio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=str, default="./output_model")
    parser.add_argument(
        "--gpt",
        type=str,
        default="llama3",
        choices=["llama3", "llama2", "phi3", "mistral"],
    )
    parser.add_argument("--isref", type=int, default=0, choices=[0, 1])
    parser.add_argument("--islog", type=int, default=1, choices=[0, 1])
    parser.add_argument("--logpath", type=str, default=r"./log")
    config = parser.parse_args()
    chatbot = chat(config)
    while True:
        input_text = input(">>> 請提問... (輸入 -1 表示結束)\n")
        if input_text.lower() == "-1":
            break
        for chunk in chatbot.ask_stream(input_text):
            if answer_chunk := chunk.get("answer"):
                print(f"{answer_chunk}|", end="")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--m", type=str, default="./output_model")
    # parser.add_argument(
    #     "--gpt",
    #     type=str,
    #     default="llama3",
    #     choices=["llama3", "llama2", "phi3", "mistral"],
    # )
    # parser.add_argument("--isref", type=int, default=0, choices=[0, 1])
    # parser.add_argument("--islog", type=int, default=1, choices=[0, 1])
    # parser.add_argument("--logpath", type=str, default=r"./log")
    # config = parser.parse_args()
    # chatbot = chat(config)
    # while True:
    #     input_text = input(">>> 請提問... (輸入 -1 表示結束)\n")
    #     if input_text.lower() == "-1":
    #         break
    #     chatbot.ask(input_text)
    main()
