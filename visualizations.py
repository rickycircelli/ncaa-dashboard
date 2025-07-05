import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Set Styles
sns.set_style('whitegrid')
sns.set_palette('muted')

# Plots time progression graph for a selected event
def plot_time_progression(df, event_filter):
    """Returns a Seaborn time progression graph as a Matplotlib figure."""
    df_event = df[df['Event'] == event_filter].dropna(subset=['Time_seconds', 'Race_Date']).copy()
    df_event = df_event.sort_values('Race_Date')

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df_event, x='Race_Date', y='Time_seconds', marker='o', linewidth=2.5, ax=ax)

    ax.invert_yaxis()
    ax.set_title(f'{event_filter}m Time Progression', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Time (seconds)', fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for i, row in df_event.iterrows():
        ax.text(row['Race_Date'], row['Time_seconds'] - 0.1, row['Mark'],
                ha='center', va='bottom', fontsize=10, color='black')

    fastest_row = df_event.loc[df_event['Time_seconds'].idxmin()]
    ax.scatter(fastest_row['Race_Date'], fastest_row['Time_seconds'],
               color='red', s=100, edgecolor='black', zorder=5, label='Fastest Time')
    
    ax.legend(title='Legend', fontsize=12, title_fontsize=13)

    return fig


# Plots placement distribution graph for all events
def plot_placement_distribution(df):
    placement_counts = df['Placement_Number'].value_counts().sort_index()
    num_no_placement = df['Placement_Number'].isna().sum()

    placement_df = pd.DataFrame({
        'Placement': placement_counts.index.astype(int).astype(str),
        'Count': placement_counts.values
    })

    placement_df = pd.concat([
        placement_df,
        pd.DataFrame({'Placement': ['No Placement'], 'Count': [num_no_placement]})
    ], ignore_index=True)

    numeric_placements = [p for p in placement_df['Placement'] if p != 'No Placement']
    numeric_placements = sorted(set(int(p) for p in numeric_placements))
    numeric_placements = [str(p) for p in numeric_placements]

    placement_df['Placement'] = pd.Categorical(
        placement_df['Placement'],
        categories=numeric_placements + ['No Placement'],
        ordered=True
    )
    placement_df = placement_df.sort_values('Placement')

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(data=placement_df, x='Placement', y='Count', hue='Placement',
                palette='muted', edgecolor='black', legend=False, ax=ax)

    ax.set_title('Placement Distribution Across All Races', fontsize=16)
    ax.set_xlabel('Finish Position', fontsize=14)
    ax.set_ylabel('Number of Races', fontsize=14)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=0)

    return fig

