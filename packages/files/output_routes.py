import pandas as pd
from files.base_output import BaseOutput


class OutputRoutes(BaseOutput):
    def export(self, trips, results):
        rows = self.get_rows(trips, results)
        self.write_excel(rows)

    def get_rows(self, trips, results):
        rows = list()
        for trip, result in zip(trips, results):
            merged_data = self.join_results(trip, result)
            rows.append(merged_data)
        return rows

    def join_results(trip, result):
        return {**trip, **result}

    def write_excel(self, data):
        dataframe = pd.DataFrame(data)
        with pd.ExcelWriter(self.output_path) as writer:
            dataframe.to_excel(writer, sheet_name="Viajes")
