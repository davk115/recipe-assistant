import os
import pandas as pd

import minsearch

data = "../data/data_clean.csv"

def load_index():
    df = pd.read_csv(data)
    df = df.replace({float('nan'): 'None'})

    documents = df.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=[
            'recipe_name',
            'cuisine_type',
            'ingredients',
            'cooking_instructions',
            'dietary_preferences',
            'difficulty'
        ],
        keyword_fields=['id'],
    )

    index.fit(documents)

    return index