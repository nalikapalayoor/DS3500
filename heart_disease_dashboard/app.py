import pandas as pd
import panel as pn
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pymysql
import plotly.express as px  
import seaborn as sns

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

connection = pymysql.connect(**db_config)

with open('data.sql', 'r') as file:
    sql_script = file.read()

with connection.cursor() as cursor:
    for statement in sql_script.split(';'):
        if statement.strip():  
            cursor.execute(statement)

connection.commit()
connection.close()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

query = "SELECT * FROM heart_table" 
df = pd.read_sql(query, engine)




pn.extension()

color_palette = ['hotpink', 'darkorange', 'springgreen', 'mediumorchid']

plot_width = 250  
plot_height = 175  
font_size = 5  

def plot_age_distribution(heart_disease_status):    
    
    if heart_disease_status == 'All':
        filtered_data = df
    elif heart_disease_status == 'Patients with Heart Disease':
        filtered_data = df[df['target'] == 'Heart Disease']
    else:
        filtered_data = df[df['target'] == 'No Heart Disease']

    plt.figure(figsize=(plot_width / 100, plot_height / 100))
    plt.hist(filtered_data['age'], bins=15, alpha=0.7, color=color_palette[0], edgecolor='black')
    plt.xlabel('Age', fontsize=font_size)
    plt.ylabel('Frequency', fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlim(df['age'].min(), df['age'].max())
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()

    return pn.pane.Matplotlib(plt.gcf(), tight=True)


heart_disease_dropdown = pn.widgets.Select(
    name='Heart Disease Status',
    options=['All', 'Patients with Heart Disease', 'Patients without Heart Disease'],
    value='All'
)

age_distribution_plot = pn.bind(plot_age_distribution, heart_disease_status=heart_disease_dropdown)

def create_treemap():
    df['sex'] = df['sex'].map({0: 'Female', 1: 'Male'})
    df['target'] = df['target'].map({0: 'No Heart Disease', 1: 'Heart Disease'})
    df['exercise_angina'] = df['exercise_angina'].map({0: 'No Angina', 1: 'Angina'})

    fig = px.treemap(df,
                     path=['sex', 'exercise_angina', 'target'],
                     values='unique_id',  
                     color='target',  
                     color_discrete_sequence=color_palette,
                     width=plot_width+20,  
                     height=plot_height+20
                     )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0) 
    )

    return pn.pane.Plotly(fig)

treemap_plot = create_treemap()

def double_bar_chart():
    df = pd.read_sql(query, engine)

    grouped_data = df.groupby(['fasting_blood_sugar', 'target']).agg({'cholesterol': 'mean'}).unstack()

    fig, ax = plt.subplots(figsize=(plot_width / 100, plot_height / 100))  
    grouped_data.plot(kind='bar', width=0.7, ax=ax, color=color_palette[:2]) 

    ax.set_xlabel('Fasting Blood Sugar', fontsize=font_size)
    ax.set_ylabel('Average Cholesterol', fontsize=font_size)
    ax.set_xticks(range(len(grouped_data)))
    ax.set_xticklabels(grouped_data.index, rotation=0, fontsize=font_size)
    ax.legend(['Without Heart Disease', 'With Heart Disease'], fontsize=font_size)

    plt.tight_layout()

    return pn.pane.Matplotlib(fig, tight=True)

double_bar = double_bar_chart()

def create_bp_violin_plot():
    df = pd.read_sql(query, engine)

    df['target'] = df['target'].map({0: 'No Heart Disease', 1: 'Heart Disease'})

    plt.figure(figsize=(plot_width / 100, plot_height / 100)) 
    sns.violinplot(x='chest_pain_type', y='resting_bp_s', hue='target', data=df, palette=color_palette[:2], split=True, inner="box", linewidth=0.8)

    plt.xlabel('Chest Pain Type', fontsize=font_size)
    plt.ylabel('Resting Blood Pressure (Systolic)', fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.legend(fontsize=font_size)  
    plt.tight_layout()

    return pn.pane.Matplotlib(plt.gcf(), tight=True)

bp_violin_plot = create_bp_violin_plot()

dashboard = pn.Column(
    "# Heart Disease Statistics <3",  

    pn.Row(
        pn.Column("### Age Distribution", age_distribution_plot),  
        pn.Column(
            "",
            "",
            heart_disease_dropdown,
            pn.pane.Markdown("<br>Select from the dropdown what<br>heart disease status you want<br>to display", margin=(0, 0, 0, 0))
        ),
        pn.Column("### Treemap of Heart Disease Factors", treemap_plot), 
        pn.Column(
            pn.pane.Markdown("<br><br><br>Exercise-induced angina is chest<br>pain caused by exercise. It can be<br>a sign of heart disease.", margin=(0, 0, 0, 0))
        )
    ),
    
    pn.Row(
        pn.Column("### Average Cholesterol by Fasting Blood Sugar", double_bar),  
        pn.Column(
            pn.pane.Markdown("<br><br><br>0 = fasting blood sugar < 120<br>1 = fasting blood sugar > 120", margin=(0, 0, 0, 0))
        ),
        pn.Column("### Resting Blood Pressure by Chest Pain Type", bp_violin_plot, margin=(0, 0, 0, 130)),  
        pn.Column(
            pn.pane.Markdown("<br><br><br>1 = Typical angina<br>2 = Atypical angina<br>3 = Non-anginal pain<br>4 = Asymptomatic<br>High blood pressure is also a risk<br>factor in heart disease", margin=(0, 0, 0, 0))
        )
    )
)

dashboard.show()
