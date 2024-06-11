import pandas as pd

# Three separate CSV files were obtained from Pubmed to split the 
# 22,773 results.
df1 = pd.read_csv('csv-extracellu-set.csv')

df2 = pd.read_csv('csv-extracellu-set(1).csv')

df3 = pd.read_csv('csv-extracellu-set(2).csv')

# Combining the three CSV files into one
combined_df = pd.concat([df1, df2, df3])

# Getting rid of any duplicate articles in the combined CSV
combined_df_unique = combined_df.drop_duplicates(subset = "PMID")

# Only want the DOIs from the CSV files for the dataframepip
doi_df = combined_df_unique[["DOI"]]

# Makes sure all the letters in the DOI are lowercase.
doi_df.loc[:, "DOI"] = doi_df["DOI"].str.lower()

# Saving the results as a CSV file.
doi_df.to_csv('pubmed_doi.csv', index = False)



