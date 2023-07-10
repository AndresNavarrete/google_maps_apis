from packages.app import App

if __name__ == "__main__":
    api_key = "AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI"
    app = App(api_key=api_key, input_file="request.xlsx", service_name="")
    app.execute()
