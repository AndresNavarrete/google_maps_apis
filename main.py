from packages.serviceLevelManager import ServiceLevelManager

if __name__ == '__main__':
    path = "resources/request.xlsx"
    apiKey = "AQUI_VA_API_KEY"
    app = ServiceLevelManager(path, apiKey)
    app.execute()
