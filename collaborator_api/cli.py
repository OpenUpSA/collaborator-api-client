from collaborator_api.client import Client
import sys


def main():
    username = sys.argv[1]
    password = sys.argv[2]
    client = Client(username, password)
    client.authenticate()
    client.new_task_feedback()


if __name__ == "__main__":
    main()
