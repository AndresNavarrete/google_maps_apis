from packages.clients.routes import Routes
from packages.enums import Field_Masks

if __name__ == "__main__":
    print(Field_Masks.string_list())
    api_key = "AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI"
    api = Routes(api_key)
    r = api.get_route(
        origin='Pachuca, Mexico',
        destination='Ciudad de México, México'
    )
    print(r.json())
