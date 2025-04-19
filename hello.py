from preswald import text, plotly, connect, get_df, table, slider
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Welcome message
text("# Depression Analysis Dashboard 📊")
text("Explore insights about depression through interactive visualizations.")

# Load the dataset
try:
    connect()
    df = get_df("sample")

    if df is None:
        print("Using pandas to load data directly as a fallback")
        df = pd.read_csv("data/sample.csv")
except Exception as e:
    print(f"Error during initialization: {e}")
    df = pd.read_csv("data/sample.csv")

# Rename columns with spaces/special characters
df.rename(columns={
    "Work/Study Hours": "Work_Study_Hours",
    "Sleep Duration": "Sleep_Duration",
    "Have you ever had suicidal thoughts ?": "Suicidal_Thoughts"  # Rename problematic column
}, inplace=True)

# --- 1. CGPA Distribution ---
text("1. Distribution of CGPA")
CGPA_min, CGPA_max = df['CGPA'].min(), df['CGPA'].max()
threshold1 = slider("Minimum CGPA", min_val=CGPA_min, max_val=CGPA_max, default=CGPA_min + 2)
filtered_df1 = df[df['CGPA'] > threshold1]

fig1 = px.histogram(filtered_df1, x="CGPA", nbins=20, title="Distribution of CGPA")
fig1.update_traces(marker_color='lightgreen')
fig1.update_layout(template='plotly_white')
plotly(fig1)

# --- 2. Age Distribution ---
text("2. Distribution of Age")
age_min, age_max = df['Age'].min(), df['Age'].max()
threshold2 = slider("Minimum Age", min_val=age_min, max_val=age_max, default=age_min + 2)
filtered_df2 = df[df['Age'] > threshold2]

fig2 = px.histogram(filtered_df2, x="Age", nbins=20, title="Distribution of Age")
fig2.update_traces(marker_color='lightgreen')
fig2.update_layout(template='plotly_white')
plotly(fig2)

# --- 3. Work/Study Hours Distribution ---
text("3. Distribution of Work/Study Hours")
work_study_hours_min, work_study_hours_max = df['Work_Study_Hours'].min(), df['Work_Study_Hours'].max()
threshold3 = slider("Minimum Work/Study Hours", min_val=work_study_hours_min, max_val=work_study_hours_max, default=work_study_hours_min + 2)
filtered_df3 = df[df['Work_Study_Hours'] > threshold3]

fig3 = px.histogram(filtered_df3, x="Work_Study_Hours", nbins=20, title="Distribution of Work/Study Hours")
fig3.update_traces(marker_color='lightgreen')
fig3.update_layout(template='plotly_white')
plotly(fig3)

# --- 4. Sleep Duration Distribution ---
text("4. Distribution of Sleep Duration")

fig4 = px.histogram(
    df,
    x="Sleep_Duration",
    nbins=20,
    title="Distribution of Sleep Duration",
    color="Depression",  # Use Depression to vary colors
    color_discrete_map={0: 'lightgreen', 1: 'red'},  # Map colors to Depression levels
    labels={"Sleep_Duration": "Sleep Duration (hours)", "Depression": "Depression Level"}
)
fig4.update_layout(
    template='plotly_white',
    xaxis_title="Sleep Duration (hours)",
    yaxis_title="Count",
    legend_title="Depression Level"
)
plotly(fig4)

# --- 5. Gender Distribution with Depression (Grouped Bar Chart) ---
text("5. Gender Distribution by Depression Level")
gender_depression_counts = df.groupby(["Gender", 'Depression']).size().reset_index(name='Count')

fig5 = px.bar(
    gender_depression_counts,
    x="Gender",
    y="Count",
    color="Depression",
    title="Gender Distribution with Depression (Grouped)",
    color_discrete_map={0: 'lightgreen', 1: 'red'},  # Map colors to Depression levels
    labels={"Count": "Number of Individuals", "Depression": "Depression Level"},
    barmode='group'  # Group bars for each gender
)
fig5.update_layout(
    template='plotly_white',
    legend_title="Depression Level"
)
plotly(fig5)

# --- 6. Degree Distribution ---
text("6. Distribution of Academic Degrees")
degree_counts = df["Degree"].value_counts().reset_index()
degree_counts.columns = ["Degree", "Count"]

fig6 = px.bar(degree_counts, x="Degree", y="Count", title="Degree Distribution")
fig6.update_traces(marker_color='lightgreen')
fig6.update_layout(template='plotly_white')
plotly(fig6)

# --- 7. Correlation Heatmap ---
text("7. Correlation Heatmap of Numeric Variables")
numeric_df = df.select_dtypes(include=['float64', 'int64'])
numeric_df = numeric_df.dropna()

corr_matrix = numeric_df.corr()

fig7 = ff.create_annotated_heatmap(
    z=corr_matrix.values,
    x=list(corr_matrix.columns),
    y=list(corr_matrix.index),
    annotation_text=corr_matrix.round(2).values,
    colorscale='Viridis'
)
fig7.update_layout(
    title="Correlation Heatmap",
    template='plotly_white',
    xaxis=dict(side="bottom")  # Place x-axis labels at the bottom
)
plotly(fig7)

# --- 8. Academic Pressure and Depression (Box Plot) ---
text("8. Academic Pressure vs Depression Level")
academic_pressure_min, academic_pressure_max = df['Academic Pressure'].min(), df['Academic Pressure'].max()
threshold8 = slider("Minimum Academic Pressure", min_val=academic_pressure_min, max_val=academic_pressure_max, default=academic_pressure_min + 2)
filtered_df8 = df[df['Academic Pressure'] > threshold8]

fig8 = px.box(
    filtered_df8,
    x="Depression",
    y="Academic Pressure",
    color="Depression",
    title="Academic Pressure Distribution by Depression Level",
    color_discrete_map={0: 'lightgreen', 1: 'red'},
    labels={
        "Depression": "Depression Level (0: No, 1: Yes)",
        "Academic Pressure": "Reported Academic Pressure"
    }
)
fig8.update_layout(
    template='plotly_white',
    xaxis_title="Depression Level",
    yaxis_title="Academic Pressure",
    legend_title="Depression Level"
)
fig8.update_xaxes(tickvals=[0, 1], ticktext=["Not Depressed", "Depressed"])
plotly(fig8)

# --- 9. Dietary Habits and Depression (Grouped Bar Chart) ---
text("9. Dietary Habits vs Depression Level")
diet_depression_counts = df.groupby(['Dietary Habits', 'Depression']).size().reset_index(name='Count')

fig9 = px.bar(
    diet_depression_counts,
    x="Dietary Habits",
    y="Count",
    color="Depression",
    title="Dietary Habits vs Depression",
    labels={"Dietary Habits": "Dietary Habits", "Depression": "Depression Level"},
    color_discrete_map={0: 'lightgreen', 1: 'red'},
    barmode='group'
)
fig9.update_layout(template='plotly_white')
fig9.update_xaxes(tickvals=[0, 1], ticktext=["Not Depressed", "Depressed"])
plotly(fig9)

# --- 10. Financial Stress and Depression (Histogram) ---
text("10. Financial Stress vs Depression Level")

fig10 = px.histogram(
    df,
    x="Financial Stress",
    nbins=20,
    title="Distribution of Financial Stress",
    color="Depression",
    color_discrete_map={0: 'lightgreen', 1: 'red'},
    labels={"Financial Stress": "Financial Stress", "Depression": "Depression Level"}
)
fig10.update_layout(
    template='plotly_white',
    xaxis_title="Financial Stress",
    yaxis_title="Count",
    legend_title="Depression Level"
)
fig10.update_xaxes(tickvals=[0, 1], ticktext=["Not Depressed", "Depressed"])
plotly(fig10)

# --- 11. Family History of Mental Illness and Depression (Grouped Bar Chart) ---
text("11. Family History of Mental Illness vs Depression Level")
family_history_counts = df.groupby(['Family History of Mental Illness', 'Depression']).size().reset_index(name='Count')

fig11 = px.bar(
    family_history_counts,
    x="Family History of Mental Illness",
    y="Count",
    color="Depression",
    title="Family History of Mental Illness vs Depression",
    labels={"Family History of Mental Illness": "Family History", "Depression": "Depression Level"},
    color_discrete_map={0: 'lightgreen', 1: 'red'},
    barmode='group'
)
fig11.update_layout(template='plotly_white')
fig11.update_xaxes(tickvals=[0, 1], ticktext=["Not Depressed", "Depressed"])
plotly(fig11)

# --- 12. Suicidal Thoughts and Depression (Grouped Bar Chart) ---
text("12. Suicidal Thoughts vs Depression Level")
suicidal_thoughts_counts = df.groupby(['Suicidal_Thoughts', 'Depression']).size().reset_index(name='Count')

fig12 = px.bar(
    suicidal_thoughts_counts,
    x="Suicidal_Thoughts",
    y="Count",
    color="Depression",
    title="Suicidal Thoughts vs Depression",
    labels={"Suicidal_Thoughts": "Suicidal Thoughts", "Depression": "Depression Level"},
    color_discrete_map={0: 'lightgreen', 1: 'red'},
    barmode='group'
)
fig12.update_layout(template='plotly_white')
fig12.update_xaxes(tickvals=[0, 1], ticktext=["Not Depressed", "Depressed"])
plotly(fig12)

# --- 13. Scatter Plot: CGPA vs Depression ---
text("13. CGPA vs Depression Level")

fig13 = px.scatter(df, x="CGPA", y="Depression",
                   title="CGPA vs Depression",
                   labels={"CGPA": "CGPA", "Depression": "Depression Level (0 or 1)"})
fig13.update_traces(marker=dict(color='red', opacity=0.6))
fig13.update_layout(template='plotly_white')
fig13.update_xaxes(tickvals=[0, 1], ticktext=["Not Depressed", "Depressed"])
plotly(fig13)