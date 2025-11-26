import pandas as pd

def check_index_column(df: pd.DataFrame) -> bool:
    """
    Checks if the first column of the DataFrame appears to be an index column.
    
    Criteria:
    1. Column name contains "Unnamed" or is empty/None.
    2. Values are unique.
    """
    if df.empty or df.shape[1] < 2:
        return False
        
    first_col_name = str(df.columns[0])
    
    # Check name criteria
    is_unnamed = "Unnamed" in first_col_name or not first_col_name or first_col_name.lower() == "id"
    
    if not is_unnamed:
        return False
        
    # Check uniqueness
    is_unique = df.iloc[:, 0].is_unique
    
    return is_unique
