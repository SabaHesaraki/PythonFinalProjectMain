import csv
import re
from model import Model


class Controller:

    def __init__(self, model=None):
        self.model = model if model else Model()
        self.current_user = None

    def login(self, username, password):
        if not username or not password:
            return False, "Username and Password are required."

        user = self.model.check_user_login(username, password)
        if user:
            self.current_user = user
            return True, f"Welcome, {user[2]}!"
        else:
            return False, "Invalid username or password."

    def validate_inputs(
        self,
        plot_name,
        plot_loc,
        plant_name,
        plant_type,
        soil_type,
        ph,
        temp,
        humidity,
    ):
        if not plot_name or not plot_loc or not plant_name:
            return False, "Plot and Plant details cannot be empty."

        ph_pattern = r"^\d+(\.\d+)?$"
        if not re.match(ph_pattern, str(ph)):
            return False, "pH must be a valid number (e.g. 6.5)."

        val_ph = float(ph)
        if val_ph < 0 or val_ph > 14:
            return False, "pH must be between 0 and 14."

        temp_pattern = r"^-?\d+(\.\d+)?$"
        if not re.match(temp_pattern, str(temp)):
            return False, "Temperature must be a valid number (e.g. 25.0)."

        hum_pattern = r"^\d+(\.\d+)?$"
        if not re.match(hum_pattern, str(humidity)):
            return False, "Humidity must be a valid number (e.g. 60)."

        val_hum = float(humidity)
        if val_hum < 0 or val_hum > 100:
            return False, "Humidity must be between 0 and 100."

        return True, "Valid"

    def save_new_entry(
        self,
        plot_name,
        plot_loc,
        plant_name,
        plant_type,
        soil_type,
        ph,
        temp,
        humidity,
        notes,
        user_id=None,
    ):
        valid, msg = self.validate_inputs(
            plot_name,
            plot_loc,
            plant_name,
            plant_type,
            soil_type,
            ph,
            temp,
            humidity,
        )
        if not valid:
            return False, msg

        try:

            actual_user_id = (
                user_id
                if user_id
                else (self.current_user[0] if self.current_user else 1)
            )

            self.model.insert_full_record(
                actual_user_id,
                plot_name,
                plot_loc,
                plant_name,
                plant_type,
                soil_type,
                float(ph),
                float(temp),
                float(humidity),
                notes,
            )
            return True, "Record saved successfully!"
        except Exception as e:
            return False, f"Database error: {e}"

    def update_entry(
        self,
        record_id,
        plot_name,
        plot_loc,
        plant_name,
        plant_type,
        soil_type,
        ph,
        temp,
        humidity,
        notes,
        user_id=None,
    ):
        if not record_id:
            return False, "Please select a record to update."

        valid, msg = self.validate_inputs(
            plot_name,
            plot_loc,
            plant_name,
            plant_type,
            soil_type,
            ph,
            temp,
            humidity,
        )
        if not valid:
            return False, msg

        try:
            self.model.update_record(
                int(record_id),
                plot_name,
                plot_loc,
                plant_name,
                plant_type,
                soil_type,
                float(ph),
                float(temp),
                float(humidity),
                notes,
            )
            return True, "Record updated successfully!"
        except Exception as e:
            return False, f"Database error: {e}"

    def delete_entry(self, record_id):
        if not record_id:
            return False, "Please select a record to delete."
        try:
            self.model.delete_record(int(record_id))
            return True, "Record deleted successfully!"
        except Exception as e:
            return False, f"Database error: {e}"

    def load_table_data(self):
        return self.model.load_table_data()

    def export_to_csv(self, filename):
        try:
            data = self.model.load_table_data()
            headers = [
                "ID",
                "Date",
                "Plot",
                "Location",
                "Plant",
                "Type",
                "Soil",
                "pH",
                "Temp",
                "Humidity",
                "Notes",
            ]
            with open(
                filename, mode="w", newline="", encoding="utf-8"
            ) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data)
            return True, f"Data exported successfully to {filename}"
        except Exception as e:
            return False, f"Export error: {e}"
