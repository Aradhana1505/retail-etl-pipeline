import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    original_len = len(df)
    logger.info(f"Starting validation: {original_len} rows")

    # 1. Rename columns — remove spaces for SQL compatibility
    df = df.rename(columns={
        'Transaction ID': 'transaction_id',
        'Date':           'date',
        'Customer ID':    'customer_id',
        'Gender':         'gender',
        'Age':            'age',
        'Product Category': 'product_category',
        'Quantity':       'quantity',
        'Price per Unit': 'price_per_unit',
        'Total Amount':   'total_amount'
    })

    # 2. Parse date column from string to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    invalid_dates = df['date'].isna().sum()
    if invalid_dates > 0:
        logger.warning(f"Dropped {invalid_dates} rows with invalid dates")
    df = df.dropna(subset=['date'])

    # 3. Encode categorical columns
    df['gender']           = df['gender'].astype('category')
    df['product_category'] = df['product_category'].astype('category')

    # 4. Ensure numeric types
    df['quantity']      = pd.to_numeric(df['quantity'],      errors='coerce')
    df['price_per_unit']= pd.to_numeric(df['price_per_unit'],errors='coerce')
    df['total_amount']  = pd.to_numeric(df['total_amount'],  errors='coerce')
    df['age']           = pd.to_numeric(df['age'],           errors='coerce')

    # 5. Drop rows with null values in critical columns
    critical_cols = ['transaction_id', 'customer_id', 'quantity', 'price_per_unit', 'total_amount']
    df = df.dropna(subset=critical_cols)

    # 6. Drop negative or zero values — business rule
    df = df[(df['quantity'] > 0) & (df['price_per_unit'] > 0) & (df['total_amount'] > 0)]

    # 7. Verify total_amount = quantity x price_per_unit
    df['calculated_total'] = df['quantity'] * df['price_per_unit']
    mismatches = df[df['calculated_total'] != df['total_amount']]
    if len(mismatches) > 0:
        logger.warning(f"{len(mismatches)} rows have total_amount mismatches — recalculating")
        df['total_amount'] = df['calculated_total']
    df = df.drop(columns=['calculated_total'])

    # 8. Add derived columns useful for KPIs later
    df['year']  = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')

    final_len = len(df)
    logger.info(f"Validation complete: {final_len} rows kept, {original_len - final_len} dropped")
    return df