from sys import argv

from packages.app import App

if __name__ == "__main__":
    api_key = "AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI"
    input_file = "request.xlsx"
    excel = False

    app = App(api_key=api_key, input_file=input_file, service_name=argv[1], excel=excel)
    app.execute()
