import pandas as pd
from datetime import datetime


# Load your dataset
# Assuming the dataset is in CSV format for this example
# df = pd.read_csv('your_dataset.csv')

# 1. Check for unexpected strings (e.g., invalid categories or patterns)
def check_unexpected_strings(df, column, expected_values):
    """
    This function checks for unexpected string values in a column.
    :param df: DataFrame containing the data
    :param column: The column to check for unexpected strings
    :param expected_values: A list of expected string values
    :return: List of unexpected values found in the column
    """
    unexpected = df[~df[column].isin(expected_values)][column].unique()
    return unexpected


# Example usage:
# Assuming a column 'category' should only have certain categories
sample_data = [{"category": 1, "category1": 2}, {"category": 5, "category1": 10},
               {"category": "Clothing", "category1": 10}]
df = pd.DataFrame(sample_data)
expected_categories = ['Clothing']
unexpected_categories = check_unexpected_strings(df, 'category', expected_categories)
print(f"Unexpected categories: {unexpected_categories}")


# 2. Check for unexpected numerical values (e.g., negative prices, or values out of range)
def check_unexpected_numerical(df, column, min_value=None, max_value=None):
    """
    This function checks for unexpected numerical values outside a specified range.
    :param df: DataFrame containing the data
    :param column: The numerical column to check
    :param min_value: Minimum allowed value
    :param max_value: Maximum allowed value
    :return: List of unexpected values found in the column
    """
    if min_value is not None:
        invalid_min = df[df[column] < min_value][column].unique()
    if max_value is not None:
        invalid_max = df[df[column] > max_value][column].unique()

    return invalid_min.tolist(), invalid_max.tolist()


# Example usage:
# Assuming 'price' should be non-negative and less than 10000
sample_data = [{"price": 1}, {"price": 50}, {"price": 50}, {"price": 100000000}, {"price": 500}]
df = pd.DataFrame(sample_data)
unexpected_prices = check_unexpected_numerical(df, 'price', min_value=100, max_value=10000)
print(f"Unexpected prices: {unexpected_prices}")


# 3. Check for unexpected dates (e.g., invalid format or out-of-range dates)
def check_unexpected_dates(df, column, date_format="%Y-%m-%d", expected_date_range=""):
    """
    This function checks for unexpected dates that are either invalid or out of range.
    :param df: DataFrame containing the data
    :param column: The date column to check
    :param date_format: The expected date format (default is YYYY-MM-DD)
    :return: List of invalid or out-of-range dates
    """
    invalid_dates = []
    for date_str in df[column]:
        try:
            # Try to parse the date using the expected format
            formated_time = datetime.strptime(date_str, date_format)
        except ValueError:
            invalid_dates.append(date_str)
        else:
            if expected_date_range is not None:
                dr = expected_date_range.split("#")
                min_date = datetime.strptime(dr[0], date_format)
                max_date = datetime.strptime(dr[1], date_format)
                if formated_time < min_date or formated_time > max_date:
                    invalid_dates.append(formated_time)
    return invalid_dates


# Example usage:
# Assuming 'order_date' should be in the format 'YYYY-MM-DD'
sample_data = [{"order_date": '2020-0101'}, {"order_date": '2020-01-02'}, {"order_date": "20200103"}]
df = pd.DataFrame(sample_data)
invalid_dates = check_unexpected_dates(df, 'order_date', expected_date_range="2020-01-02#2020-01-02")
print(f"Invalid dates: {invalid_dates}")


# 4. Ensure data integrity with joins (e.g., foreign key validation)
def check_missing_references(df1, df2, key1, key2):
    """
    This function checks for missing references between two DataFrames based on key columns.
    :param df1: First DataFrame to check (e.g., main data)
    :param df2: Second DataFrame to check (e.g., reference data)
    :param key1: Key column in df1
    :param key2: Key column in df2
    :return: List of missing references in df1
    """
    missing = df1[~df1[key1].isin(df2[key2])][key1].unique()
    return missing


# Example usage:
# Assuming df1 contains 'product_id' and df2 contains the valid 'product_id' values
sample_data1 = [{"product_id": 1}, {"product_id": 2}, {"product_id": 3}]
df1 = pd.DataFrame(sample_data1)
sample_data2 = [{"product_id": 2}, {"product_id": 3}, {"product_id": 5}]
df2 = pd.DataFrame(sample_data2)

missing_products = check_missing_references(df1, df2, 'product_id', 'product_id')
print(f"Missing product references: {missing_products}")


# 5. Test for edge cases (e.g., null values, empty strings, large datasets)
def check_edge_cases(df, column):
    """
    This function checks for edge cases such as null values or empty strings in a column.
    :param df: DataFrame containing the data
    :param column: The column to check for edge cases
    :return: Dictionary containing counts of null, empty, and other edge cases
    """
    null_count = df[column].isnull().sum()
    empty_count = (df[column] == '').sum()
    return {
        'null_count': int(null_count),
        'empty_count': int(empty_count)
    }


# Example usage:
# Check for null or empty values in 'customer_name'
sample_data = [{"customer_name": "zhangsan"}, {"customer_name": "lisi"}, {"customer_name": "wangwu"},
               {"customer_name": ""},{"customer_name": ""}, {"customer_name": None}]
df = pd.DataFrame(sample_data)
edge_cases = check_edge_cases(df, 'customer_name')
print(f"Edge cases for 'customer_name': {edge_cases}")
