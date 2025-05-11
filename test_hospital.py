import unittest
import os
import json
from Hospital import MedicalHistory, Patient, DiagnosisRecord


class TestHospital(unittest.TestCase):
    def setUp(self):
        """Set up a temporary JSON file for testing."""
        self.test_file = "test_medical_records.json"
        self.history = MedicalHistory(self.test_file)
        # Create a clean test file
        with open(self.test_file, "w") as file:
            json.dump({"patients": []}, file)

    def tearDown(self):
        """Clean up the temporary JSON file after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_patient(self):
        """Test adding a patient with medical records."""
        patient = Patient("P001", "John Doe", "1990-01-01", "Male")
        record = DiagnosisRecord("Flu")
        self.history.add_patient(patient, [record])

        # Load data and verify
        patients = self.history.load_data()
        self.assertEqual(len(patients), 1)
        self.assertEqual(patients[0]["patient_id"], "P001")
        self.assertEqual(patients[0]["records"][0]["diagnosis"], "Flu")

    def test_display_patients(self):
        """Test displaying patients."""
        patient = Patient("P002", "Jane Doe", "1985-05-15", "Female")
        record = DiagnosisRecord("Cold")
        self.history.add_patient(patient, [record])

        # Capture printed output
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output
        self.history.display_patients()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Patient ID: P002", output)
        self.assertIn("Diagnosis: Cold", output)

    def test_load_data_empty(self):
        """Test loading data from an empty file."""
        patients = self.history.load_data()
        self.assertEqual(patients, [])

    def test_save_data(self):
        """Test saving data to the JSON file."""
        patient = Patient("P003", "Alice Smith", "2000-12-12", "Female")
        record = DiagnosisRecord("Allergy")
        self.history.add_patient(patient, [record])

        # Verify the file content
        with open(self.test_file, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data["patients"]), 1)
        self.assertEqual(data["patients"][0]["name"], "Alice Smith")
        self.assertEqual(data["patients"][0]["records"][0]["diagnosis"], "Allergy")


if __name__ == "__main__":
    unittest.main()