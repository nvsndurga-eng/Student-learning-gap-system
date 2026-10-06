import pandas as pd

def analyze_students(csv_path):
    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = df.columns.str.strip()

    # Assume first column is Student Identifier
    student_col = df.columns[0]

    # Detect subject columns (numeric only)
    subject_cols = []
    for col in df.columns[1:]:
        if pd.api.types.is_numeric_dtype(df[col]):
            subject_cols.append(col)

    if len(subject_cols) == 0:
        raise ValueError("No numeric subject columns found in CSV")

    results = []

    for _, row in df.iterrows():
        marks = row[subject_cols]
        avg = marks.mean()

        gaps = []
        for sub in subject_cols:
            if row[sub] < df[sub].mean():
                gaps.append(sub)

        # Risk logic (generic)
        if avg < 45:
            risk = "High"
        elif avg < 65:
            risk = "Medium"
        else:
            risk = "Low"

        results.append({
            "Student": row[student_col],
            "Average": round(avg, 2),
            "Gaps": ", ".join(gaps),
            "Risk": risk
        })

    return results
