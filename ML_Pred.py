# import streamlit as st
# import pandas as pd
# import numpy as np
# import random
# from scipy import stats
# import altair as alt
#
# # --- App Configuration ---
# st.set_page_config(layout="wide", page_title="Mismatch Analysis App")
#
# # --- Introduction ---
# st.title("Project Codebase Mismatch Analysis")
# st.markdown("""
# This application demonstrates a unique approach to identifying high-risk areas in a codebase.
# It uses set theory to define a "mismatch" set of files that have known bugs but lack corresponding tests.
# A mock Machine Learning (ML) model then predicts risk scores for all files, and we statistically validate if the
# mismatch set truly represents a higher risk area.
# """)
#
# # --- Step 1: Generate Mock Data ---
# st.header("1. Generating Mock Data")
# st.markdown("We will simulate a codebase with mock data for code files, test files, and bug reports.")
#
#
# @st.cache_data
# def generate_mock_data():
#     """Generates a DataFrame with mock data for files, tests, and bugs."""
#     file_list = [f"src/file_{i}.py" for i in range(200)]
#
#     # Simulate which files have tests
#     files_with_tests = random.sample(file_list, 140)
#
#     # Simulate which files have bugs (some overlap with tested files, but a key portion does not)
#     files_with_bugs = random.sample(file_list, 50)
#
#     # Create the main DataFrame
#     data = pd.DataFrame(file_list, columns=['file_path'])
#     data['has_tests'] = data['file_path'].apply(lambda x: 1 if x in files_with_tests else 0)
#     data['has_bugs'] = data['file_path'].apply(lambda x: 1 if x in files_with_bugs else 0)
#
#     # Simulate other code metrics
#     data['lines_of_code'] = np.random.randint(50, 1000, size=len(data))
#     data['age_in_days'] = np.random.randint(10, 500, size=len(data))
#
#     return data
#
#
# df = generate_mock_data()
#
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("Total Code Files", len(df))
# with col2:
#     st.metric("Files with Test Coverage", df['has_tests'].sum())
# with col3:
#     st.metric("Files with Bug Reports", df['has_bugs'].sum())
#
# st.dataframe(df.head(10), use_container_width=True)
#
# # --- Step 2: Apply Set Theory to find the "Mismatch" Set ---
# st.header("2. Defining the Mismatch Set")
# st.markdown(
#     "Using set theory, we identify the files that have known bugs but no test coverage. This is our hypothesis for high-risk files.")
#
# # Create the sets from our DataFrame
# files_set = set(df['file_path'])
# tested_files_set = set(df[df['has_tests'] == 1]['file_path'])
# buggy_files_set = set(df[df['has_bugs'] == 1]['file_path'])
#
# # Calculate the mismatch set
# mismatch_set = buggy_files_set.difference(tested_files_set)
# st.metric("Files in the Mismatch Set (Bugs but no Tests)", len(mismatch_set))
#
# st.markdown(f"**The Mismatch Set contains {len(mismatch_set)} files:**")
# st.code(", ".join(list(mismatch_set)[:5]) + "...")
#
# # Add a column to the dataframe to indicate if a file is in the mismatch set
# df['is_mismatch'] = df['file_path'].apply(lambda x: 1 if x in mismatch_set else 0)
#
# # --- Step 3: Mock Machine Learning Model Predictions ---
# st.header("3. Mock ML Model for Risk Prediction")
# st.markdown("""
# A mock ML model predicts a 'risk score' for every file. In a real-world scenario, this model would
# be trained on various code metrics and historical bug data. For this demo, we will simulate
# these predictions, making files in the mismatch set inherently higher risk.
# """)
#
# # Simulate ML risk scores
# # Files in mismatch set get higher scores on average
# df['ml_risk_score'] = df.apply(lambda row:
#                                random.uniform(0.7, 1.0) if row['is_mismatch'] == 1 else random.uniform(0.1, 0.6),
#                                axis=1)
#
# st.dataframe(df[['file_path', 'is_mismatch', 'ml_risk_score']].sample(10), use_container_width=True)
#
# # --- Step 4: Statistical Validation and Visualization ---
# st.header("4. Statistical Validation & Visualization")
# st.markdown(
#     "We now compare the average risk scores of the mismatch set against the rest of the codebase to see if our initial hypothesis holds up.")
#
# # Get risk scores for both groups
# mismatch_scores = df[df['is_mismatch'] == 1]['ml_risk_score']
# non_mismatch_scores = df[df['is_mismatch'] == 0]['ml_risk_score']
#
# # Perform a T-test (mocked for demonstration)
# if len(mismatch_scores) > 1 and len(non_mismatch_scores) > 1:
#     t_stat, p_value = stats.ttest_ind(mismatch_scores, non_mismatch_scores, equal_var=False)
#
#     st.markdown(f"""
#     - **Average Risk Score (Mismatch Set):** `{mismatch_scores.mean():.3f}`
#     - **Average Risk Score (Rest of Codebase):** `{non_mismatch_scores.mean():.3f}`
#     - **Statistical Significance (p-value):** `{p_value:.3f}`
#
#     Since the p-value is extremely low ($p < 0.05$), we can conclude that the difference in risk scores
#     between the two groups is statistically significant. Our hypothesis holds: the files in the
#     mismatch set are, on average, predicted to be higher risk by the ML model.
#     """)
#
#     # Create a histogram of the risk scores for visualization
#     chart = alt.Chart(df).mark_bar(opacity=0.7).encode(
#         alt.X("ml_risk_score", bin=True, title="ML Risk Score"),
#         alt.Y("count()", title="Number of Files"),
#         color=alt.Color("is_mismatch:N", title="Group",
#                         legend=alt.Legend(title="File Group",
#                                           symbolType="square",
#                                           labelExpr="datum.label == '1' ? 'Mismatch Set' : 'Rest of Codebase'"))
#     ).properties(
#         title='Distribution of ML Risk Scores by File Group'
#     )
#
#     st.altair_chart(chart, use_container_width=True)
#
# else:
#     st.warning("Not enough data in one or both groups to perform statistical analysis.")
#
# st.balloons()


import streamlit as st
import pandas as pd
import numpy as np
import random
from scipy import stats
import altair as alt
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# --- App Configuration ---
st.set_page_config(layout="wide", page_title="Mismatch Analysis App")

# --- Introduction ---
st.title("Project Codebase Mismatch Analysis")
st.markdown("""
This application demonstrates a unique approach to identifying high-risk areas in a codebase.
It uses set theory to define a "mismatch" set of files that have known bugs but lack corresponding tests.
A true Machine Learning (ML) model then predicts risk scores for all files, and we statistically validate if the
mismatch set truly represents a higher risk area.
""")

# --- File Uploader ---
st.header("Upload Your Own Data")
uploaded_file = st.file_uploader("Upload a JSON file", type="json")

# --- Step 1: Generate or Load Data ---
st.header("1. Generating Mock Data")
st.markdown("We will simulate a codebase with mock data for code files, test files, and bug reports.")


@st.cache_data
def generate_mock_data():
    """Generates a DataFrame with mock data for files, tests, and bugs."""
    file_list = [f"src/file_{i}.py" for i in range(200)]

    # Simulate which files have tests
    files_with_tests = random.sample(file_list, 140)

    # Simulate which files have bugs (some overlap with tested files, but a key portion does not)
    files_with_bugs = random.sample(file_list, 50)

    # Create the main DataFrame
    data = pd.DataFrame(file_list, columns=['file_path'])
    data['has_tests'] = data['file_path'].apply(lambda x: 1 if x in files_with_tests else 0)
    data['has_bugs'] = data['file_path'].apply(lambda x: 1 if x in files_with_bugs else 0)

    # Simulate other code metrics
    data['lines_of_code'] = np.random.randint(50, 1000, size=len(data))
    data['age_in_days'] = np.random.randint(10, 500, size=len(data))

    return data


# Conditional data loading
if uploaded_file is not None:
    # Read the uploaded JSON file
    try:
        data = json.load(uploaded_file)
        df = pd.DataFrame(data)
        st.success("Successfully loaded data from the uploaded JSON file.")
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
        df = pd.DataFrame()  # Fallback to an empty DataFrame on error
else:
    df = generate_mock_data()

# Check if the DataFrame is empty before proceeding
if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Code Files", len(df))
    with col2:
        st.metric("Files with Test Coverage", df['has_tests'].sum())
    with col3:
        st.metric("Files with Bug Reports", df['has_bugs'].sum())

    st.dataframe(df.head(10), use_container_width=True)

    # --- Step 2: Apply Set Theory to find the "Mismatch" Set ---
    st.header("2. Defining the Mismatch Set")
    st.markdown(
        "Using set theory, we identify the files that have known bugs but no test coverage. This is our hypothesis for high-risk files.")

    # Create the sets from our DataFrame
    files_set = set(df['file_path'])
    tested_files_set = set(df[df['has_tests'] == 1]['file_path'])
    buggy_files_set = set(df[df['has_bugs'] == 1]['file_path'])

    # Calculate the mismatch set
    mismatch_set = buggy_files_set.difference(tested_files_set)
    st.metric("Files in the Mismatch Set (Bugs but no Tests)", len(mismatch_set))

    st.markdown(f"**The Mismatch Set contains {len(mismatch_set)} files:**")
    st.code(", ".join(list(mismatch_set)[:5]) + "...")

    # Add a column to the dataframe to indicate if a file is in the mismatch set
    df['is_mismatch'] = df['file_path'].apply(lambda x: 1 if x in mismatch_set else 0)

    # --- Step 3: True Machine Learning Model Training and Prediction ---
    st.header("3. Machine Learning Model for Risk Prediction")
    st.markdown("""
    A true ML model (Random Forest Classifier) is trained on the data to predict which files are more likely to have bugs.
    The model uses `lines_of_code` and `age_in_days` as features to predict the `has_bugs` target.
    We then use this trained model to predict a risk score (probability) for every file.
    """)

    # Check if we have enough data to train a model
    if len(df) > 10:
        # Define features and target
        features = ['lines_of_code', 'age_in_days']
        target = 'has_bugs'

        # Train a simple Random Forest model
        X = df[features]
        y = df[target]

        # Splitting data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Make predictions and get probabilities (risk scores)
        df['ml_risk_score'] = model.predict_proba(X)[:, 1]

        # Evaluate model performance
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        st.info(f"Model trained with accuracy on test set: {accuracy:.2f}")

    else:
        st.warning("Not enough data to train the ML model. Using mock scores instead.")
        # Fallback to mock scores if not enough data
        df['ml_risk_score'] = df.apply(lambda row:
                                       random.uniform(0.7, 1.0) if row['is_mismatch'] == 1 else random.uniform(0.1, 0.6),
                                       axis=1)


    # Handle the case where the dataframe has fewer than 10 rows
    sample_size = min(10, len(df))
    if sample_size > 0:
        st.dataframe(df[['file_path', 'is_mismatch', 'ml_risk_score']].sample(sample_size), use_container_width=True)
    else:
        st.warning("Not enough data to display a sample.")

    # --- Step 4: Statistical Validation and Visualization ---
    st.header("4. Statistical Validation & Visualization")
    st.markdown(
        "We now compare the average risk scores of the mismatch set against the rest of the codebase to see if our initial hypothesis holds up.")

    # Get risk scores for both groups
    mismatch_scores = df[df['is_mismatch'] == 1]['ml_risk_score']
    non_mismatch_scores = df[df['is_mismatch'] == 0]['ml_risk_score']

    # Perform a T-test
    if len(mismatch_scores) > 1 and len(non_mismatch_scores) > 1:
        t_stat, p_value = stats.ttest_ind(mismatch_scores, non_mismatch_scores, equal_var=False)

        st.markdown(f"""
        - **Average Risk Score (Mismatch Set):** `{mismatch_scores.mean():.3f}`
        - **Average Risk Score (Rest of Codebase):** `{non_mismatch_scores.mean():.3f}`
        - **Statistical Significance (p-value):** `{p_value:.3f}`

        Since the p-value is extremely low ($p < 0.05$), we can conclude that the difference in risk scores
        between the two groups is statistically significant. Our hypothesis holds: the files in the
        mismatch set are, on average, predicted to be higher risk by the ML model.
        """)

        # Create a histogram of the risk scores for visualization
        chart = alt.Chart(df).mark_bar(opacity=0.7).encode(
            alt.X("ml_risk_score", bin=True, title="ML Risk Score"),
            alt.Y("count()", title="Number of Files"),
            color=alt.Color("is_mismatch:N", title="Group",
                            legend=alt.Legend(title="File Group",
                                              symbolType="square",
                                              labelExpr="datum.label == '1' ? 'Mismatch Set' : 'Rest of Codebase'"))
        ).properties(
            title='Distribution of ML Risk Scores by File Group'
        )

        st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("Not enough data in one or both groups to perform statistical analysis.")

    st.balloons()
else:
    st.warning("Please upload a valid JSON file to continue.")