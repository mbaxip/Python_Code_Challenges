"""
Analyzes the immune cell population data of melanoma patients and 
identifies the cell populations significantly responding to treatment tr1.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.stats.multitest as smm
import warnings
warnings.filterwarnings('ignore')

# Load data
data = pd.read_csv('./cell-count.csv')
data.head()
data.shape

populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']


def convert_cellcount_to_relative_freq_perc(populations, df):
    """Convert cell count to relative frequency (%) """

    for cell_pop in populations:
        df[cell_pop + '_rel_freq'] = df[cell_pop]/data['total_count'] * 100
    return df


def boxplot_fig(df):
    """ Creates Box-plot of the population relative frequencies comparing responders vs non-responders for tr1 """
    plt.figure()

    sns.boxplot(x=df['population'],
                y=df['percentage'],
                hue=df['response'])

    plt.xlabel("Cell Population")
    plt.ylabel("Relative Frequency %")
    plt.title("Population relative frequency: Responders vs Non-responders to treatment tr1")

    return plt


def t_test(populations, df):
    """ Conducts a t-test to identify which cell population shows a significant difference
    between responders and non-responders """
    pvalues_pop = []
    for cell_pop in populations:
        group1 = df[(df['population'] == cell_pop) & (df['response'] == 'y')]
        group2 = df[(df['population'] == cell_pop) & (df['response'] == 'n')]
        t_stat, p_value = stats.ttest_ind(group1['percentage'], group2['percentage'])
        pvalues_pop.append(p_value)

    # FDR correction to adjust the p-values (multiple comparisons correction)
    corrected_p_values = smm.fdrcorrection(pvalues_pop)[1]
    return corrected_p_values


if __name__ == '__main__':
    ''' 
    1.	Please write a python program to convert cell count in cell-count.csv to relative frequency (in percentage) of 
    total cell count for each sample. 
    Total cell count of each sample is the sum of cells in the five populations of that sample. 
    Please return an output file in csv format with cell count and relative frequency of each population
    of each sample per line. 
    The output file should have the following columns:

    sample: the sample id as in column sample in cell-count.csv
    total_count: total cell count of sample
    population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
    count: cell count
    percentage: relative frequency in percentage
    '''

    # Compute total count of each sample: sum of cell counts in five populations
    data['total_count'] = data[populations].sum(axis=1)

    # Convert cell count to relative frequency (%)
    data = convert_cellcount_to_relative_freq_perc(populations, data)

    # Create new dataframe to be stored as output with cell count and relative frequency of each population
    #  of each sample per line
    new_df = pd.melt(data, id_vars=['sample', 'total_count'], value_vars=populations,
                     var_name='population', value_name='count')
    temp_perc = []
    for cell_pop in populations:
        temp_perc.extend(data[cell_pop + '_rel_freq'])
    new_df['percentage'] = temp_perc

    # Save the output file
    new_df.to_csv('./cell-count-relative-freq.csv', index=False)

    '''
    2.	Among patients who have treatment tr1, we are interested in comparing the differences in cell population relative 
    frequencies of melanoma patients who respond (responders) to tr1 versus those who do not (non-responders), with the 
    overarching aim of predicting response to treatment tr1. Response information can be found in column response, with 
    value y for responding and value n for non-responding. Please only include PBMC (blood) samples. 

    a.	For each immune cell population, please generate a boxplot of the population relative frequencies 
    comparing responders versus non-responders.

    b.	Which cell populations show a difference between responders and non-responders? 
    Please include statistics to support your conclusion.

    '''
    # Filter patients with PBMC blood samples that were given treatment tr1
    data_tr1 = data[(data['treatment'] == 'tr1') & (data['sample_type'] == 'PBMC')]

    # Drop samples with response na
    data_tr1 = data_tr1.dropna(subset=['response'])

    # Filter the output dataframe with relative frequency of each cell population per line
    new_df_tr1 = new_df[new_df['sample'].isin(data_tr1['sample'])]

    # Add response variable to the filtered output dataframe
    temp_resp = list(data_tr1['response']) * len(populations)
    new_df_tr1['response'] = temp_resp
    new_df_tr1.reset_index(inplace=True, drop=True)

    # Box-plot of the population relative frequencies comparing responders vs non-responders for tr1
    plot = boxplot_fig(new_df_tr1)
    plot.show()

    # T-test to identify which cell population shows a significant difference between responders and non-responders
    p_values = t_test(populations, new_df_tr1)

    # Result: Print Cell populations showing significant difference between responders and non-responders
    index = [ind for ind, x in enumerate(list(p_values)) if x < 0.05]
    signif_diff_pop = [populations[i] for i in index]
    print('Cell populations showing significant difference between responders and non-responders: ', signif_diff_pop)
