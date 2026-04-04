PREDEFINED_CONDITIONS = [
    # Metabolic
    {"id": "type1_diabetes", "label": "Type 1 Diabetes", "category": "Metabolic"},
    {"id": "type2_diabetes", "label": "Type 2 Diabetes", "category": "Metabolic"},
    {"id": "hypothyroidism", "label": "Hypothyroidism", "category": "Metabolic"},
    {"id": "hyperthyroidism", "label": "Hyperthyroidism", "category": "Metabolic"},
    {"id": "obesity", "label": "Obesity", "category": "Metabolic"},
    {"id": "pcod", "label": "PCOD / PCOS", "category": "Metabolic"},
    # Respiratory
    {"id": "tuberculosis", "label": "Tuberculosis (TB)", "category": "Respiratory"},
    {"id": "asthma", "label": "Asthma", "category": "Respiratory"},
    {"id": "copd", "label": "COPD", "category": "Respiratory"},
    {"id": "chronic_bronchitis", "label": "Chronic Bronchitis", "category": "Respiratory"},
    {"id": "sleep_apnea", "label": "Sleep Apnea", "category": "Respiratory"},
    # Cardiovascular
    {"id": "hypertension", "label": "Hypertension (High BP)", "category": "Cardiovascular"},
    {"id": "heart_disease", "label": "Coronary Heart Disease", "category": "Cardiovascular"},
    {"id": "heart_failure", "label": "Heart Failure", "category": "Cardiovascular"},
    {"id": "arrhythmia", "label": "Arrhythmia", "category": "Cardiovascular"},
    {"id": "high_cholesterol", "label": "High Cholesterol", "category": "Cardiovascular"},
    # Mental Health
    {"id": "depression", "label": "Depression", "category": "Mental Health"},
    {"id": "anxiety", "label": "Anxiety Disorder", "category": "Mental Health"},
    {"id": "bipolar", "label": "Bipolar Disorder", "category": "Mental Health"},
    {"id": "ocd", "label": "OCD", "category": "Mental Health"},
    {"id": "ptsd", "label": "PTSD", "category": "Mental Health"},
    # Digestive
    {"id": "gerd", "label": "GERD / Acid Reflux", "category": "Digestive"},
    {"id": "ibs", "label": "IBS", "category": "Digestive"},
    {"id": "crohns", "label": "Crohn's Disease", "category": "Digestive"},
    {"id": "ulcerative_colitis", "label": "Ulcerative Colitis", "category": "Digestive"},
    {"id": "celiac", "label": "Celiac Disease", "category": "Digestive"},
    # Musculoskeletal
    {"id": "rheumatoid_arthritis", "label": "Rheumatoid Arthritis", "category": "Musculoskeletal"},
    {"id": "osteoarthritis", "label": "Osteoarthritis", "category": "Musculoskeletal"},
    {"id": "osteoporosis", "label": "Osteoporosis", "category": "Musculoskeletal"},
    {"id": "gout", "label": "Gout", "category": "Musculoskeletal"},
    # Neurological
    {"id": "epilepsy", "label": "Epilepsy", "category": "Neurological"},
    {"id": "migraine", "label": "Chronic Migraines", "category": "Neurological"},
    {"id": "parkinsons", "label": "Parkinson's Disease", "category": "Neurological"},
    {"id": "multiple_sclerosis", "label": "Multiple Sclerosis", "category": "Neurological"},
    # Kidney / Liver
    {"id": "ckd", "label": "Chronic Kidney Disease", "category": "Kidney/Liver"},
    {"id": "kidney_stones", "label": "Kidney Stones", "category": "Kidney/Liver"},
    {"id": "fatty_liver", "label": "Fatty Liver Disease", "category": "Kidney/Liver"},
    {"id": "hepatitis_b", "label": "Hepatitis B", "category": "Kidney/Liver"},
    {"id": "hepatitis_c", "label": "Hepatitis C", "category": "Kidney/Liver"},
    # Skin
    {"id": "psoriasis", "label": "Psoriasis", "category": "Skin"},
    {"id": "eczema", "label": "Eczema / Atopic Dermatitis", "category": "Skin"},
    # Other
    {"id": "anemia", "label": "Anemia", "category": "Other"},
    {"id": "hiv", "label": "HIV / AIDS", "category": "Other"},
    {"id": "lupus", "label": "Lupus (SLE)", "category": "Other"},
    {"id": "cancer", "label": "Cancer (any type)", "category": "Other"},
]

CONDITION_IDS = {c["id"] for c in PREDEFINED_CONDITIONS}
