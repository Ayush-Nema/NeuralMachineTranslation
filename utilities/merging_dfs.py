import glob
import uuid
import pandas as pd


def df_merger(df_path):
    merged_df = pd.DataFrame()
    for i in glob.glob(df_path):
        this_df = pd.read_csv(i)
        merged_df = merged_df.append(this_df)

    merged_df['intent'] = 'knowledge'
    merged_df['source'] = 'ml-20211025'
    return merged_df


def compile_df(compilation_path):
    merged_df = pd.DataFrame()
    for j in glob.glob(compilation_path):
        j_th_df = pd.read_csv(j)
        merged_df = merged_df.append(j_th_df)

    print(f'Size of merged_df: {merged_df.shape}')
    return generate_id(merged_df)


def generate_id(df):
    final_vals_list = df[["utterance",
                          "intent",
                          "subintent",
                          "source"]].values.tolist()
    insert_vals = [tuple([str(uuid.uuid4())] + record) for record in final_vals_list]

    cols_order = ['id', 'utterance', 'intent', 'subintent', 'source']
    output_df = pd.DataFrame(insert_vals, columns=cols_order)
    output_df['entities'] = '{}'
    return output_df


if __name__ == '__main__':
    df_path0 = "../data/translated_text_fr/*"
    # compiled_df = df_merger(df_path0)
    # compiled_df.to_csv('../data/translated_merged_dfs/knowledge_fr.csv', index=False)

    # Merging fr and es tables
    compile_path = '../data/translated_merged_dfs/knowledge_*.csv'
    one_df = compile_df(compile_path)

    one_df.to_csv('../data/translated_merged_dfs/one_df.csv', index=False)
