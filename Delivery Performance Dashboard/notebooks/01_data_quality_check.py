
import pandas as pd
from pathlib import Path

# Import dataset

# Find the project folder automatically
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Build the dataset path
RAW_FILE = PROJECT_DIR / "Data" / "Raw" / "Delivery_Logistics.csv"

# Check whether the file exists
print("Looking for dataset at:", RAW_FILE)

if not RAW_FILE.exists():
    print("File not found. Check the folder and filename.")
else:
    df = pd.read_csv(RAW_FILE)
    print("\nDataset imported successfully!")
    print("Dataset shape:", df.shape)
    print(df.head())

# 1. Dataset dimensions
print("\n--- DATASET SHAPE ---")
print(df.shape)

# 2. Column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 3. Data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

# 4. Missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 5. Duplicate rows
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

# 6. Duplicate delivery IDs
print("\n--- DUPLICATE DELIVERY IDs ---")
print(df["delivery_id"].duplicated().sum())

# 7. First five records
print("\n--- FIRST FIVE RECORDS ---")
print(df.head())

# -----------------------------------
# Numerical data validation
# -----------------------------------

numeric_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_rating",
    "delivery_cost"
]

print("\n--- NUMERICAL VALIDATION ---")

for column in numeric_columns:

    print(f"\nColumn: {column}")

    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())

    print(
        "Missing values:",
        df[column].isnull().sum()
    )

    print(
        "Negative values:",
        (df[column] < 0).sum()
    )

# -----------------------------------
# Check delivery rating
# -----------------------------------

print("\n--- DELIVERY RATING VALIDATION ---")

invalid_ratings = df[
    (df["delivery_rating"] < 1)
    | (df["delivery_rating"] > 5)
]

print("Invalid ratings:", len(invalid_ratings))

# -----------------------------------
# Check delivery cost
# -----------------------------------

print("\n--- DELIVERY COST VALIDATION ---")

invalid_cost = df[
    df["delivery_cost"] <= 0
]

print("Invalid delivery costs:", len(invalid_cost))

# -----------------------------------
# Categorical data inspection
# -----------------------------------

categorical_columns = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "delayed",
    "delivery_status"
]

print("\n--- CATEGORICAL VALUE INSPECTION ---")

for column in categorical_columns:

    print(f"\nColumn: {column}")

    print("Unique values:", df[column].nunique())

    print(df[column].value_counts())


# -----------------------------------
# Check extra spaces
# -----------------------------------

print("\n--- EXTRA SPACE CHECK ---")

for column in categorical_columns:

    extra_spaces = df[column].astype(str).str.strip().ne(
        df[column].astype(str)
    ).sum()

    print(column, ":", extra_spaces)

# -----------------------------------
# Standardize categorical columns
# -----------------------------------

# Create a separate working copy
df_clean = df.copy()

categorical_columns = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "delayed",
    "delivery_status"
]

print("\n--- STANDARDIZING CATEGORIES ---")

for column in categorical_columns:

    # Remove leading/trailing spaces
    # Convert text to lowercase
    df_clean[column] = (
        df_clean[column]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    print(f"\n{column}")
    print(df_clean[column].value_counts())


# -----------------------------------
# Validate categorical cleaning
# -----------------------------------

print("\n--- CATEGORICAL VALIDATION ---")

for column in categorical_columns:

    print(
        column,
        "Unique categories:",
        df_clean[column].nunique()
    )

    print(
        "Missing values:",
        df_clean[column].isnull().sum()
    )

# -----------------------------------
# Delivery ID investigation
# -----------------------------------

print("\n--- DELIVERY ID INVESTIGATION ---")

# Count occurrences of each ID
id_counts = df["delivery_id"].value_counts()

# Find IDs appearing more than once
repeated_ids = id_counts[id_counts > 1]

print("\nRepeated delivery IDs:")
print(repeated_ids)

print("\nTotal repeated ID values:", len(repeated_ids))

# Show records having repeated IDs
duplicate_id_records = df[
    df["delivery_id"].isin(repeated_ids.index)
].copy()

print(
    "\nRecords with repeated IDs:",
    len(duplicate_id_records)
)

# Check whether these records are completely identical
print(
    "\nCompletely identical records among repeated IDs:",
    duplicate_id_records.duplicated().sum()
)

# Check decimal IDs
decimal_id_records = df[
    df["delivery_id"] % 1 != 0
].copy()

print(
    "\nRecords with decimal IDs:",
    len(decimal_id_records)
)

print("\nDecimal ID values:")
print(
    decimal_id_records["delivery_id"]
    .value_counts()
)

# Save investigation reports
PROJECT_DIR = Path(__file__).resolve().parent.parent

REPORT_DIR = PROJECT_DIR / "data" / "cleaned"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

duplicate_id_records.to_csv(
    REPORT_DIR / "duplicate_id_records.csv",
    index=False
)

decimal_id_records.to_csv(
    REPORT_DIR / "decimal_id_records.csv",
    index=False
)

print("\nInvestigation reports saved successfully.")

# -----------------------------------
# Step 1.8: Create unique record IDs
# -----------------------------------

# Create a separate cleaned copy
df_clean = df.copy()

# Preserve the original delivery ID
df_clean["delivery_id_original"] = df_clean["delivery_id"]

# Create a unique ID for every record
df_clean["delivery_record_id"] = [
    f"DLV-{i:05d}"
    for i in range(1, len(df_clean) + 1)
]

# Check the new IDs
print("\n--- NEW DELIVERY RECORD ID ---")

print("Total records:", len(df_clean))

print(
    "Unique record IDs:",
    df_clean["delivery_record_id"].nunique()
)

print(
    "Duplicate new IDs:",
    df_clean["delivery_record_id"].duplicated().sum()
)

print("\nFirst 5 record IDs:")
print(
    df_clean[
        ["delivery_record_id", "delivery_id_original"]
    ].head()
)


# -----------------------------------
# Save stage 1 cleaned copy
# -----------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

CLEANED_DIR = PROJECT_DIR / "Data" / "Cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = CLEANED_DIR / "delivery_data_stage1.csv"

df_clean.to_csv(OUTPUT_FILE, index=False)

print("\nStage 1 file saved successfully!")
print("Saved location:", OUTPUT_FILE)


# -----------------------------------
# Step 1.9: Investigate delivery time
# -----------------------------------

print("\n--- DELIVERY TIME INVESTIGATION ---")

print("\nActual delivery time:")
print(df_clean["delivery_time_hours"].value_counts())

print("\nExpected delivery time:")
print(df_clean["expected_time_hours"].value_counts())

print("\nUnique actual delivery times:")
print(df_clean["delivery_time_hours"].nunique())

print("\nUnique expected delivery times:")
print(df_clean["expected_time_hours"].nunique())

# Check whether both columns contain the same values
same_time_values = (
    df_clean["delivery_time_hours"]
    == df_clean["expected_time_hours"]
).sum()

print(
    "\nRecords where actual and expected times are equal:",
    same_time_values
)
# -----------------------------------
# Step 1.9: Handle corrupted time data
# -----------------------------------

print("\n--- HANDLING DELIVERY TIME DATA ---")

# Preserve the original values for audit purposes
df_clean["delivery_time_hours_original"] = (
    df_clean["delivery_time_hours"]
)

df_clean["expected_time_hours_original"] = (
    df_clean["expected_time_hours"]
)

# These columns contain 00:00.0 in every row.
# Mark the unusable analysis values as missing.
df_clean["delivery_time_hours"] = pd.NA
df_clean["expected_time_hours"] = pd.NA

# Add a note explaining the data limitation
df_clean["time_data_quality"] = (
    "unusable_original_values"
)

print(
    "Actual delivery time values available:",
    df_clean["delivery_time_hours"].notna().sum()
)

print(
    "Expected delivery time values available:",
    df_clean["expected_time_hours"].notna().sum()
)

print(
    "Original actual-time values preserved:",
    df_clean["delivery_time_hours_original"].notna().sum()
)

print("\nTime data handled.")


# -----------------------------------
# Save Stage 2 cleaned dataset
# -----------------------------------

OUTPUT_FILE = CLEANED_DIR / "delivery_data_stage2.csv"

df_clean.to_csv(OUTPUT_FILE, index=False)

print("\nStage 2 file saved successfully!")
print("Saved location:", OUTPUT_FILE)
