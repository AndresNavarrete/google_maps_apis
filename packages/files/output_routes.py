import pandas as pd

from packages.files.base_output import BaseOutput


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

    def join_results(self, trip, result):
        trip_vars = vars(trip)
        result_vars = vars(result)
        return {**trip_vars, **result_vars}

    def write_excel(self, data):
        dataframe = pd.DataFrame(data)
        with pd.ExcelWriter(self.output_path) as writer:
            dataframe.to_excel(writer, sheet_name="Viajes")
