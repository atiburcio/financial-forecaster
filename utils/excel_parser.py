import pandas as pd
from typing import Tuple, Dict, Any, Optional
import io

def parse_excel(file: bytes) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Parse an Excel file and return its data and metadata.
    
    Args:
        file (bytes): The uploaded file content as bytes
        
    Returns:
        tuple: (DataFrame with the data, Dict with metadata)
    """
    try:
        # Read Excel file
        xls = pd.ExcelFile(io.BytesIO(file))
        
        # Get sheet names
        sheet_names = xls.sheet_names
        
        # Read first sheet by default
        df = pd.read_excel(xls, sheet_name=sheet_names[0])
        
        # Get column names and types
        column_info = [
            {
                'name': col,
                'type': str(df[col].dtype),
                'sample': df[col].iloc[0] if len(df) > 0 else None
            }
            for col in df.columns
        ]
        
        # Prepare metadata
        metadata = {
            'sheet_names': sheet_names,
            'columns': [col['name'] for col in column_info],
            'column_info': column_info,
            'n_rows': len(df),
            'date_columns': [col['name'] for col in column_info 
                           if pd.api.types.is_datetime64_any_dtype(df[col['name']]) or 
                           col['type'].startswith('datetime')]
        }
        
        return df, metadata
        
    except Exception as e:
        raise ValueError(f"Error parsing Excel file: {str(e)}")

def detect_date_column(df: pd.DataFrame, threshold: float = 0.8) -> Optional[str]:
    """
    Try to automatically detect the date column in a DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        threshold (float): Minimum ratio of datetime-like values to consider a column as date
        
    Returns:
        str or None: Name of the detected date column, or None if not found
    """
    for col in df.columns:
        # Skip columns with non-string/object types that aren't datetime
        if not pd.api.types.is_object_dtype(df[col]) and not pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
            
        # Try to convert to datetime
        try:
            date_series = pd.to_datetime(df[col], errors='coerce')
            valid_ratio = date_series.notna().mean()
            
            if valid_ratio >= threshold:
                return col
        except:
            continue
            
    return None

def detect_numeric_columns(df: pd.DataFrame, exclude_columns: list = None) -> list:
    """
    Detect numeric columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        exclude_columns (list, optional): Columns to exclude from detection
        
    Returns:
        list: List of numeric column names
    """
    if exclude_columns is None:
        exclude_columns = []
        
    numeric_cols = []
    
    for col in df.columns:
        if col in exclude_columns:
            continue
            
        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
            continue
            
        # Try to convert to numeric
        try:
            pd.to_numeric(df[col])
            numeric_cols.append(col)
        except:
            continue
            
    return numeric_cols
