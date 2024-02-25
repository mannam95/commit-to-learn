from io import StringIO
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# A function that accepts a train, test file and returns the evaluation metrics
def model_train_test_by_given_files(train_file, test_file):
    try:
        # Load train and test data
        # Convert CSV content to DataFrame
        train_df = pd.read_csv(train_file.file)
        test_df = pd.read_csv(test_file.file) if test_file else None

        # Prepare train and test features and labels
        # Read all cols except the last one as features
        # Read the last col as label
        X_train = train_df.iloc[:, :-1]
        y_train = train_df.iloc[:, -1]

        # if test_df is None, then split the train_df into train and test
        if test_df is None:
            X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
        else:
            X_test = test_df.iloc[:, :-1]
            y_test = test_df.iloc[:, -1]

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict prices
        y_pred = model.predict(X_test)

        # Calculate evaluation metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # return evaluation metrics
        return {
            "Mean Absolute Error (MAE)": mae,
            "Mean Squared Error (MSE)": mse,
            "R-squared (R2) Score": r2
        }
    except Exception as e:
        return {"error at model_train_test_by_given_files": str(e)}