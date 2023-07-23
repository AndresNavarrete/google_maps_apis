from sys import argv
import os
from packages.app import App

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    input_file = "request.xlsx"
    excel = True

    app = App(api_key=api_key, input_file=input_file, service_name=argv[1], excel=excel)
    app.execute()
