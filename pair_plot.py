import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

root = Path("datasets")
root.mkdir(exist_ok=True)

def load_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    return df

def generate_pair_plot(df, color_by=None):
    sns.set(style="ticks")
    if color_by:
        plot_data = sns.pairplot(df, hue=color_by)
    else:
        plot_data = sns.pairplot(df)
    return plot_data

def get_available_datasets():
    dataset_files = root.glob("*.csv")
    return [dataset.stem for dataset in dataset_files]

st.title("Pair Plot Explorer")

st.sidebar.title("Options")

available_datasets = get_available_datasets()

if not available_datasets:
    st.warning("No datasets found in the 'datasets' folder. Please upload a dataset.")
    uploaded_file = st.file_uploader("Upload a new dataset (CSV)", type="csv")
    if uploaded_file is not None:
        with open(root / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded and added dataset: {uploaded_file.name}")
else:
    selected_dataset = st.sidebar.selectbox("Select a dataset", available_datasets)
    df = load_dataset(root / (selected_dataset + ".csv"))

    show_color_by_option = st.sidebar.checkbox("Color by a categorical column")
    if show_color_by_option:
        color_by = st.sidebar.selectbox("Select a categorical column to use as color by", df.columns)
    else:
        color_by = None

    st.write("Upload your own dataset")
    uploaded_file = st.file_uploader("Upload a new dataset (CSV)", type="csv")
    if uploaded_file is not None:
        with open(root / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded and added dataset: {uploaded_file.name}")

    st.write("Dataset Summary")
    st.write(df.head())

    st.title("Pair Plot")
    pair_plot = generate_pair_plot(df.select_dtypes(include="number"), color_by)
    st.pyplot(pair_plot)

