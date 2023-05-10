import pandas as pd
import ast
from tqdm.auto import tqdm
import random


df_merged = pd.read_csv(r'C:\Coding_Projects\MovieLens_dataset\create_triplets_dataset\merged_clean_final.csv', encoding='utf-8')
df_merged['descriptors'] = df_merged['descriptors'].apply(ast.literal_eval)

# define a function to lowercase each string in the 'descriptors' list and convert it into a set
def process_descriptors(row):
    descriptors = row['descriptors']
    return row['movieId'], set(map(str.lower, descriptors))

# create a list of tuples from the 'movieId' and processed 'descriptors' columns
result = list(df_merged.apply(process_descriptors, axis=1))


def create_dataframe_2(tuples):
    data = []
    for anchor in tqdm(tuples):
        positives = [t for t in tuples if t[0] != anchor[0]]
        positives.sort(key=lambda x: len(x[1].intersection(anchor[1])), reverse=True)
        positive = positives[0]
        negatives = [t for t in tuples if t[0] != anchor[0] and t[0] != positive[0]]
        negatives.sort(key=lambda x: len(x[1].intersection(anchor[1])))
        negative = random.choice(negatives[:3])
        data.append((anchor[0], positive[0], negative[0]))
    df = pd.DataFrame(data, columns=['anchor', 'positive', 'negative'])
    return df

df_siam = create_dataframe_2(result)

df_siam.to_csv(r'C:\Coding_Projects\MovieLens_dataset\create_triplets_dataset\triplets_dataset.csv', encoding='utf-8')