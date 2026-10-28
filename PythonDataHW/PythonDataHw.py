import pandas as pd
import numpy as np

# 1. Load the dataset
input_file = "messy_ecommerce_sales_data.csv"
output_file = "cleaned_ecommerce_sales_data.csv"
df = pd.read_csv(input_file)

print(f"Initial dataset shape: {df.shape}")

# 2. Remove duplicates
duplicate_rows = df[df.duplicated(keep="first")]
num_duplicates = len(duplicate_rows)
print(f"Dupplicates removed: {num_duplicates}")

# Save dropped duplicates to inspect or report
df = df.drop_duplicates(keep="first").reset_index(drop=True)

# 3. Data Formatting and Type Consistency

# Data Columns
if "date" in df.columns:
    # errors='coerce' will convert invalid parsing to NaT
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

# String formatting
string_columns = df.select_dtypes(include=["object"]).columns
for col in string_columns: 
    if col != "date":
        df[col] = df[col].str.strip()

# Currency/price cleaning
if "price" in df.columns:
    df["price"] = (df["price"].astype(str).str.replace(r"[\$,]", "", regex=True))
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Outlier Handling
if "price" in df.columns:
    # Cap negative prices or invalid values to median
    price_median = df.loc[df["price"] > 0, "price"].median()
    df.loc[df["price"] <= 0, "price"] = price_median

# Remove outliers using quantiles
if "quantity" in df.columns:
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    q_low = df["quantity"].quantile(0.01)
    q_high = df["quantity"].quantile(0.99)
    df["quantity"] = df["quantity"].clip(lower=max(1, q_low), upper=q_high)

# Missing Values Imputation

# Categorical columns: Fill missing values with mode
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].replace(["nan", "None", ""], np.nan)
    df[col] = df[col].fillna("Unknown")

# Numeric columns: Fill missing values with median or mean
for col in df.select_dtypes(include=[np.number]).columns:
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)

# Export Cleaned Data
df.to_csv(output_file, index=False)
print(f"Cleaning complete. Cleaned dataset saved to {output_file}. Final dataset shape: {df.shape}")