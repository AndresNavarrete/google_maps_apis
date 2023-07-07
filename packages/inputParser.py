import pandas
import json


class InputParser:
    def __init__(self, input_path):
        self.input_path = input_path
        self.input_data = None
        self.load_input()
    
    def load_input(self):
        df = pandas.read_excel(self.input_path, sheet_name="Viajes")
        input_json = df.to_json(orient='records')
        self.requests = json.loads(input_json)
