from packages.enums import User_Modes


class Validator:
    def __init__(self, input_data):
        self.input_data = input_data
        self.ids = []
        self.modes = User_Modes.list()

    def validate_input(self):
        for request in self.input_data.requests:
            self.validate_mode(request)
            self.validate_id(request)
            self.validate_origin(request)
            self.validate_destination(request)

    def validate_mode(self, request):
        if request["Modo"] in self.modes:
            return
        msg = f"Invalid mode. id {request['ID']} mode {request['Modo']}"
        raise ValueError(msg)

    def validate_id(self, request):
        if request["ID"] in self.ids:
            msg = f"Duplicated ID. id {request['ID']}"
            raise ValueError(msg)
        self.ids.append(request["ID"])

    def validate_origin(self, request):
        if request["Origen_str"] is not None:
            return
        if request["Origen_Lat"] is None or request["Origen_Lng"] is None:
            msg = f"Invalid origin. id {request['ID']}"
            raise ValueError(msg)

    def validate_destination(self, request):
        if request["Destino_str"] is not None:
            return
        if request["Destino_Lat"] is None or request["Destino_Lng"] is None:
            msg = f"Invalid destination. id {request['ID']}"
            raise ValueError(msg)
