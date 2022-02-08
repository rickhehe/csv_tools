'''
It converts src to a string for re.X
'''

import re

import pandas as pd


def get_pattern(src):
    '''
    src to be a csv file
    '''
    src_df = pd.read_csv(src)

    y = [
        f'{x.pattern}  # {x.description}'
            for x in src_df.itertuples()
    ]

    y = '\n|\n'.join(y)

    return y
    

if __name__ == '__main__':
    src = r'src\test_pattern.csv'
    pattern = get_pattern(src)
    
    df = pd.DataFrame(
        {
            'parent': ['ba', 'b', 'ab', 'c'],
            'description': ['haha','haha','haha','haha']
        }
    )
    
    print(pattern)
        
    df_ok = df[df.parent.str.contains(pattern, flags=re.I|re.X)]
    df_ng = df[~df.parent.str.contains(pattern, flags=re.I|re.X)]

    print(df_ok)
    print(df_ng)
    
