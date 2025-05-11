import json
from abc import ABC, abstractmethod
from typing import List, Dict
import time
from functools import wraps


def timing_decorator(func):
    """
    A decorator to measure the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper


class MedicalRecord(ABC):
    """
    Abstract base class for medical records.
    Defines the structure for all types of medical records.
    """

    def __init__(self, diagnosis: str):
        self.diagnosis = diagnosis

    @abstractmethod
    def display_details(self):
        """Display the details of the medical record."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convert the medical record to a dictionary."""
        pass


class DiagnosisRecord(MedicalRecord):
    """
    Represents a diagnosis record with details about the diagnosis.
    """

    def __init__(self, diagnosis: str):
        super().__init__(diagnosis)

    def display_details(self):
        print(f"Diagnosis: {self.diagnosis}")

    def to_dict(self) -> Dict:
        return {
            "type": "diagnosis",
            "diagnosis": self.diagnosis,
        }


class Patient:
    """
    Represents a patient with personal details and a list of medical records.
    """

    def __init__(self, patient_id: str, name: str, dob: str, gender: str):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender

    def to_dict(self) -> Dict:
        """Convert the patient to a dictionary."""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
        }

    def display_info(self):
        """Display the patient's details."""
        print(f"\nPatient ID: {self.patient_id}")
        print(f"Name: {self.name}")
        print(f"Date of Birth: {self.dob}")
        print(f"Gender: {self.gender}")


class MedicalHistory:
    """
    Manages a collection of patients and their medical histories.
    """

    def __init__(self, filename: str):
        self.filename = filename

    @timing_decorator
    def load_data(self) -> List[Dict]:
        """Load patient data from the JSON file."""
        try:
            with open(self.filename, "r") as file:
                return json.load(file).get("patients", [])
        except FileNotFoundError:
            print("No existing data file found. Starting with an empty database.")
            return []

    @timing_decorator
    def save_data(self, patients: List[Dict]):
        """Save patient data to the JSON file."""
        with open(self.filename, "w") as file:
            json.dump({"patients": patients}, file, indent=4)

    def add_patient(self, patient: Patient, records: List[MedicalRecord]):
        """Add a patient and their records to the JSON file."""
        patients = self.load_data()
        patient_dict = patient.to_dict()
        patient_dict["records"] = [record.to_dict() for record in records]
        patients.append(patient_dict)
        self.save_data(patients)

    @timing_decorator
    def display_patients(self):
        """Display all patients and their records."""
        patients = self.load_data()
        for patient_data in patients:
            patient = Patient(
                patient_data["patient_id"],
                patient_data["name"],
                patient_data["dob"],
                patient_data["gender"],
            )
            patient.display_info()
            print("\nMedical Records:")
            for record_data in patient_data.get("records", []):
                if record_data["type"] == "diagnosis":
                    record = DiagnosisRecord(record_data["diagnosis"])
                    record.display_details()
                    print("-" * 30)


def main():
    history = MedicalHistory(r"C:\Users\Anatoli\Desktop\1 TB HW folder\Python\medical_records.json")

    while True:
        print("\nMedical History Management")
        print("1. View Patients")
        print("2. Add Patient")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            history.display_patients()
        elif choice == "2":
            patient_id = input("Enter patient ID: ")
            name = input("Enter patient name: ")
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            gender = input("Enter gender: ")

            patient = Patient(patient_id, name, dob, gender)
            records = []

            while True:
                add_record = input("Add a diagnosis record? (y/n): ").lower()
                if add_record == "y":
                    diagnosis = input("Enter diagnosis: ")
                    record = DiagnosisRecord(diagnosis)
                    records.append(record)
                else:
                    break

            history.add_patient(patient, records)
            print("Patient added successfully!")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()