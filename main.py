from packages.service_level_manager import ServiceLevelManager

if __name__ == "__main__":
    path = "resources/request.xlsx"
    api_key = "AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI"
    app = ServiceLevelManager(path, api_key)
    app.execute()
