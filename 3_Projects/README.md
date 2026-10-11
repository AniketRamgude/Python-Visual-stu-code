Welcome to my Data Analytics Project, where I am trying to help new data analysts find good job opportunities based on location, required skills, and the pay they want in this competitive job market. Things are changing daily in Data Analytics, and there is no single newsletter where they can easily find the jobs they want or the skills they need to improve to land the best role. I am trying to solve that problem with this project. :)

The data sourced from Luke Barousse's Python Course which provides a foundation for my analysis, containing detailed information on job titles, salaries, locations, and essential skills. 


These are the questions that make it hard for Data Analysts to find jobs, so I am working on answering them.

1.What are the skills most in demand for the top 3 most popular data roles?
2.How are in-demand skills trending for Data Analysts?
3.How well do jobs and skills pay for Data Analysts?
4.What are the optimal skills for data analysts to learn? (High Demand & High Paying)

This are the tools that, I used.

Python:  Python is backbone of this project.
Pandas Library: Pandas is used to analyze the data.
Matplotlib Library: Matplotlib heelped me to visualize my data.(Very helpful tool, makes data intresting to see!)
Seaborn Library: Helps me to build more advance visuals.
Visual Studio Code: I used this to run my Python scripts.


I started by importing the required libraries and cleaning the dataset.

# Importing Libraries
    import ast
    import pandas as pd
    import seaborn as sns
    from datasets import load_dataset
    import matplotlib.pyplot as plt  

# Loading Data
dataset = load_dataset('lukebarousse/data_jobs')
df = dataset['train'].to_pandas()

# Data Cleanup
df['job_posted_date'] = pd.to_datetime(df['job_posted_date'])
df['job_skills'] = df['job_skills'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)

I filtered the data for jobs in India.
