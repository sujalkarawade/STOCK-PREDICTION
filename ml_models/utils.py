import os
import pandas as pd

def _load_and_prep(filepath, start_date=None, end_date=None):
    extension = os.path.splitext(filepath)[1].lower()
    data = pd.read_csv(filepath) if extension == ".csv" else pd.read_excel(filepath)

    # 1. Auto-detect Date Column
    date_col_name = None
    if "Date" in data.columns:
        date_col_name = "Date"
    else:
        # Check for datetime columns
        for col in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[col]):
                date_col_name = col
                break
        if not date_col_name:
            # Try to parse string columns as dates
            for col in data.columns:
                if data[col].dtype == 'object':
                    try:
                        # Attempt to parse the first non-null value to see if it's a date
                        sample = data[col].dropna().iloc[0]
                        pd.to_datetime(sample)
                        date_col_name = col
                        break
                    except:
                        pass
    
    if date_col_name:
        data["Date"] = pd.to_datetime(data[date_col_name], errors="coerce")
    else:
        # Generate dummy dates
        data["Date"] = pd.date_range(start="2020-01-01", periods=len(data))
        date_col_name = "Index"

    # 2. Auto-detect Target Column
    target_col_name = None
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    if "Date" in numeric_cols:
        numeric_cols.remove("Date")
    if date_col_name in numeric_cols:
        numeric_cols.remove(date_col_name)

    if not numeric_cols:
        raise ValueError("No numeric columns found to predict.")

    if "Close" in numeric_cols:
        target_col_name = "Close"
    elif "Target" in numeric_cols:
        target_col_name = "Target"
    elif "y" in numeric_cols:
        target_col_name = "y"
    else:
        target_col_name = numeric_cols[-1]

    data["Close"] = pd.to_numeric(data[target_col_name], errors="coerce")
    
    # 3. Clean and prepare
    data = data.dropna(subset=["Date", "Close"]).sort_values("Date").copy()

    if len(data) < 2:
        raise ValueError("At least two valid rows with data are required.")

    # Apply date range filtering if provided
    if start_date:
        start_date = pd.to_datetime(start_date)
        data = data[data["Date"] >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        data = data[data["Date"] <= end_date]

    if len(data) < 2:
        raise ValueError("Not enough data points in the selected date range.")

    data["Days"] = (data["Date"] - data["Date"].min()).dt.days
    
    # Calculate technical indicators (Moving Averages)
    data["MA_20"] = data["Close"].rolling(window=20).mean()
    data["MA_50"] = data["Close"].rolling(window=50).mean()
    data["MA_200"] = data["Close"].rolling(window=200).mean()
    
    # Store original column names so we can use them in the UI and graphs
    data.attrs["target_col_name"] = target_col_name
    data.attrs["date_col_name"] = date_col_name
    
    return data

def _calculate_volatility_and_changes(data):
    """Calculate percentage changes."""
    metrics = {}
    
    # Daily percentage changes
    data["Daily_Change_%"] = data["Close"].pct_change() * 100
    metrics["avg_daily_change"] = round(data["Daily_Change_%"].mean(), 4)
    
    # Weekly and monthly percentage changes
    if len(data) >= 7:
        first_price = data["Close"].iloc[0]
        prices_7d_ago = data["Close"].iloc[-7] if len(data) >= 7 else first_price
        metrics["7day_change_%"] = round(((data["Close"].iloc[-1] - prices_7d_ago) / prices_7d_ago) * 100, 4)
    else:
        metrics["7day_change_%"] = 0.0
    
    if len(data) >= 30:
        prices_30d_ago = data["Close"].iloc[-30] if len(data) >= 30 else data["Close"].iloc[0]
        metrics["30day_change_%"] = round(((data["Close"].iloc[-1] - prices_30d_ago) / prices_30d_ago) * 100, 4)
    else:
        metrics["30day_change_%"] = 0.0
    
    overall_change = ((data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0]) * 100
    metrics["overall_change_%"] = round(overall_change, 4)
    
    return metrics
