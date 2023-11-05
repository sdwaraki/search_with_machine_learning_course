import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

# Useful if you want to perform stemming.
import nltk


def stem_query(query):
    tokens = query.split()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)


stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/fasttext/labeled_queries.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])


# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
queries_df = pd.read_csv(queries_file_name)[['category', 'query']]
queries_df = queries_df[queries_df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
#lowercase
queries_df['query'] = queries_df['query'].str.lower()
#treat anything that is not a number or letter as a space
queries_df['query'] = queries_df['query'].str.replace('[^a-zA-Z0-9]', ' ', regex=True)
#trim multiple spaces
queries_df['query']  = queries_df['query'].str.replace('\s+', ' ', regex=True)
#use nltk stemmer
queries_df['query'] = queries_df['query'].apply(stem_query)

# Compute the query counts for all of the categories
grouped_categories = queries_df.groupby('category').size().reset_index(name='counts')
# print(grouped_categories.columns)

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
initial_grouped_categories = queries_df.groupby('category').size().reset_index(name='counts')
print(f'initial_category_count = {initial_grouped_categories.size}')

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
while True:
    # compute grouped categories
    grouped_categories = queries_df.groupby('category').size().reset_index(name='counts')
    categories_with_count_lt_min_queries = grouped_categories[grouped_categories['counts'] < min_queries].sort_values(by=['counts'])
    #print(categories_with_count_lt_1000.size)

    # if there are no categories with count < 1000 then exit
    if categories_with_count_lt_min_queries.empty:
        break
    
    # find the category with the lowest count 
    category_with_lowest_count = grouped_categories.loc[categories_with_count_lt_min_queries['counts'].idxmin(), 'category']

    #find the parent of that category
    parent_category = parents_df[parents_df['category'] == category_with_lowest_count].values[0][1]

    #replace all category with the lowest count with the parent category in queries_df
    queries_df['category'] = queries_df['category'].replace(category_with_lowest_count, parent_category)


final_grouped_categories = queries_df.groupby('category').size().reset_index(name='counts')
print(f'final_category_count = {final_grouped_categories.size}')

# Create labels in fastText format.
queries_df['label'] = '__label__' + queries_df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
queries_df = queries_df[queries_df['category'].isin(categories)]
queries_df['output'] = queries_df['label'] + ' ' + queries_df['query']
queries_df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)

