import app
from chat import get_default_chat_instance


def main():
    app.start_server(get_default_chat_instance())


if "__main__" == __name__:
    main()
