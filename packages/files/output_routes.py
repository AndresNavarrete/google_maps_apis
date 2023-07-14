import json

import pandas as pd

from packages.files.base_output import BaseOutput


class OutputRoutes(BaseOutput):
    def export(self, trips, results, excel):
        rows = self.get_rows(trips, results)
        if excel:
            self.write_excel(rows)
        self.export_json(rows)

    def get_rows(self, trips, results):
        rows = list()
        for trip, result in zip(trips, results):
            merged_data = self.join_results(trip, result)
            rows.append(merged_data)
        return rows

    def join_results(self, trip, result):
        trip_vars = vars(trip)
        result_vars = vars(result)
        return {**trip_vars, **result_vars}

    def write_excel(self, data):
        path = f"{self.output_path}.xlsx"
        dataframe = pd.DataFrame(data)
        with pd.ExcelWriter(path) as writer:
            dataframe.to_excel(writer, sheet_name="Viajes")

    def export_json(self, data):
        path = f"{self.output_path}.json"
        with open(path, "w") as f:
            json.dump(data, f)
