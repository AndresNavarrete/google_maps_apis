from packages.clients.routes import Routes
from packages.enums import Field_Masks

if __name__ == "__main__":
    print(Field_Masks.string_list())
    api_key = "AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI"
    api = Routes(api_key)
    r = api.get_route(
        origin='2da B Juárez 102, Los Jales, Ex Hacienda de Coscotitlán, 42064 Pachuca de Soto, Hgo., Mexico',
        destination='Calz. de Tlalpan 3465, Sta. Úrsula Coapa, Coyoacán, 04650 Ciudad de México, CDMX, Mexico'
    )
    print(r.json())
