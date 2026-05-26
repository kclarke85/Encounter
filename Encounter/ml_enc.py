# ml_streamlit_dashboard.py
import json
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


# Path to your JSON file
JSON_PATH = r"C:\Users\kclar\PycharmProjects\VOZ_trigger\synthetic_sensor_data.json"


# Load and preprocess data
def load_data(json_path):
   with open(json_path, 'r') as f:
       raw = json.load(f)
   df = pd.DataFrame(raw)
   df['timestamp'] = pd.to_datetime(df['timestamp'])
   return df


def extract_features(df):
   df['delta_accel_mag'] = df['accel_mag'].diff().abs().fillna(0)
   df['delta_gyro_mag'] = df['gyro_mag'].diff().abs().fillna(0)


   df['prev_state'] = df['state'].shift(1)
   df['rest_to_extreme_flag'] = ((df['prev_state'] == 'rest') & (df['state'] == 'extreme')).astype(int)


   df['state_change'] = (df['state'] != df['prev_state']).astype(int)
   df['state_change_rate'] = df['state_change'].rolling(window=10).sum().fillna(0)


   df['time_in_rest'] = 0
   counter = 0
   for i, row in df.iterrows():
       if row['state'] == 'rest':
           counter += 1
       else:
           counter = 0
       df.at[i, 'time_in_rest'] = counter


   df = df.dropna().reset_index(drop=True)
   return df


def prepare_data(df):
   feature_cols = ['accel_mag', 'gyro_mag', 'delta_accel_mag', 'delta_gyro_mag',
                   'rest_to_extreme_flag', 'state_change_rate', 'time_in_rest']
   label_col = 'state'
   X = df[feature_cols]
   y = df[label_col]
   return train_test_split(X, y, test_size=0.3, random_state=42)


# Streamlit app
st.title("VOZ Trigger: Sensor Insight Dashboard")
st.markdown("Visualization and ML analysis from synthetic MPU-6050 data")


df = load_data(JSON_PATH)
df = extract_features(df)


# Data visualizations
st.subheader("Raw Sensor State Distribution")
st.bar_chart(df['state'].value_counts())


st.subheader("Acceleration & Gyroscope Magnitude Over Time")
st.line_chart(df.set_index('timestamp')[['accel_mag', 'gyro_mag']])


st.subheader("State Change Rate Over Time")
st.line_chart(df.set_index('timestamp')['state_change_rate'])


# ML Model
X_train, X_test, y_train, y_test = prepare_data(df)


clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)


# Show classification report
st.subheader("Classification Report")
report = classification_report(y_test, y_pred, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose())


# Feature importance chart
st.subheader("Feature Importance")
importance_df = pd.DataFrame({
   'Feature': X_train.columns,
   'Importance': clf.feature_importances_
}).sort_values(by='Importance', ascending=False)
st.bar_chart(importance_df.set_index('Feature'))


# Predictions
st.subheader("Sample Predictions")
sample_df = X_test.copy()
sample_df['True State'] = y_test.values
sample_df['Predicted State'] = y_pred
st.dataframe(sample_df.head(50))




