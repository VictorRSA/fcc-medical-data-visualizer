#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################
# Created by: Joao Pedro Peters Barbosa #
#                                       #
# github: https://github.com/Jppbrbs    #
# email: jpptrs@gmail.com               #
#                                       #
# Date: Jul/2020                        #
#########################################


"""
freeCodeCamp Project3 - Data Analysis with Python Course
"""



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
overweight = (df['weight'] / ((df['height'] / 100)**2) > 25).astype(int)
# print(overweight)
df['overweight'] = overweight

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
# print(df['cholesterol'])
df['gluc'] = (df['gluc'] > 1).astype(int)

# print(df['gluc'])
# print(df.info())


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=[
            'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'
        ])
    # print(df_cat)

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = pd.DataFrame(
        df_cat.groupby(['cardio', 'variable',
                        'value'])['value'].count()).rename(columns={
                            'value': 'total'
                        }).reset_index()
    # print(df_cat)

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar')

    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])
                 & (df['height'] >= df['height'].quantile(0.025))
                 & (df['height'] <= df['height'].quantile(0.975))
                 & (df['weight'] >= df['weight'].quantile(0.025))
                 & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(
        corr,
        linewidths=.5,
        annot=True,
        fmt='.1f',
        mask=mask,
        square=True,
        center=0,
        vmin=-0.1,
        vmax=0.25,
        cbar_kws={
            'shrink': .45,
            'format': '%.2f'
        })

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
