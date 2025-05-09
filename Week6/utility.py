import logging
import yaml
import re

def replacer(col, pattern):
    return re.sub(pattern, '', col)

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            logging.error(exc)

def col_header_val(df, table_config):
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x, '_'), list(df.columns)))

    expected_col = list(map(lambda x: x.lower(), table_config['columns']))
    expected_col.sort()
    df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis=1)

    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print("Column name and length validation passed")
        return 1
    else:
        print("Column name and length validation failed")
        mismatched_columns_file = list(set(df.columns).difference(expected_col))
        print("File columns not in YAML:", mismatched_columns_file)
        missing_yaml_columns = list(set(expected_col).difference(df.columns))
        print("YAML columns not in file:", missing_yaml_columns)
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
