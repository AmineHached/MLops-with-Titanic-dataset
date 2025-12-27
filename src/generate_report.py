from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Titanic MLOps Pipeline Report', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_report():
    pdf = PDF()
    pdf.add_page()
    
    # Toolchain
    pdf.chapter_title("1. Architecture & Toolchain")
    pdf.chapter_body("The pipeline uses a robust MLOps stack:\n- Git: Version control for code.\n- DVC: Data versioning and pipeline orchestration.\n- MLflow: Experiment tracking and model registry.\n- GitHub Actions: CI/CD automation.\n- Scikit-Learn: Machine learning modeling.")
    
    # Dataset Versioning
    pdf.chapter_title("2. Dataset Versioning Strategy")
    pdf.chapter_body("Three versions were created:\n- V1: Raw Titanic data (handled nulls/encoding in code).\n- V2: Cleaned data (Age/Fare scaled, missing values handled).\n- V3: Feature engineered data (Family size, Title extraction).")
    
    # Pipeline Stages
    pdf.chapter_title("3. Pipeline Stages")
    pdf.chapter_body("The DVC pipeline (dvc.yaml) automates:\n1. clean_data -> 2. feature_engineering -> 3. training -> 4. registration.")
    
    # Model Comparison
    pdf.chapter_title("4. Model Comparison Results")
    pdf.chapter_body("Logistic Regression: F1 ~0.74\nRandom Forest: F1 ~0.80\nNote: Random Forest outperformed Logistic Regression in this experiment.")
    
    # Advanced Feature
    pdf.chapter_title("5. Advanced Feature: Automatic Model Selection")
    pdf.chapter_body("A custom script (register_model.py) automatically identifies the run with the highest F1-score and registers it in the MLflow Model Registry, promoting it to 'Production'.")
    
    # Conclusion
    pdf.chapter_title("6. Conclusion")
    pdf.chapter_body("This project demonstrates a production-grade MLOps setup, ensuring reproducibility and automated governance for machine learning models.")
    
    pdf.output("MLOps_Titanic_Report.pdf")
    print("Report generated: MLOps_Titanic_Report.pdf")

if __name__ == "__main__":
    generate_report()
