import pandas as pd

from datetime_tricks import datetime_csv_suffix

def spliter(df, col, min_block_size):
    
    df.sort_values(by=col, inplace=True)
    df.reset_index().drop(columns=['index'], inplace=True)

    container = []

    r, c = df.shape
    while r > min_block_size:
        df.reset_index(inplace=True)
        df.drop(columns=['index'], inplace=True)

        for i in range(min_block_size, r-1):

            if df[col].iloc[i] != df[col].iloc[i+1]:
                break

        else:
            raise Exception('oversize')

        container.append(df[:i+1])

        df = df[i+1:]
        r, c = df.shape

    container.append(df)

    return container

def export_splitted(container):

    len_container = len(container)

    for i, item in enumerate(container, start=1):
        item.to_csv(
            datetime_csv_suffix(
                f'c:/vba_output/{i}_of_{len_container}.csv'
            ),
            index=None
        )

def export_parent_csv(df):

    # just incase some x's are lower case letters.
    df = df.apply(lambda x: x.astype(str).str.upper())

    df.set_index('parent', inplace = True)

    # create csv files. aka bom.  Filename = parent.
    for i in df.index.unique():
        df_i = df[df.index == i]
        if df_i.empty:
            print(f'{i} is empty DataFrame')
            break
        else:
            df_i.to_csv(f'output\\{i}.csv', index = None)

if __name__ == '__main__':

    d = {
        'parent':list('abbaaaacbbccdddeeeff')
    }
    
    df = pd.DataFrame(d)
    print(df)
    
    y = spliter(df, 'parent', 7)
    for i in y:
        print(i)
    #export_splitted(y)
