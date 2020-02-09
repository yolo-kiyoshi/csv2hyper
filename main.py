import os
import json
import sys

from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, NOT_NULLABLE, NULLABLE, SqlType, TableDefinition, escape_string_literal


# SqlTypeをdictで参照
sql_type_dict = {}
sql_type_dict['BIG_INT'] = SqlType.big_int()
sql_type_dict['TEXT'] = SqlType.text()
sql_type_dict['DOUBLE'] = SqlType.double()
sql_type_dict['DATE'] = SqlType.date()
sql_type_dict['TIMESTAMP'] = SqlType.timestamp()
# NULLABLEをdictで参照
nullable_dict = {}
nullable_dict['YES'] = NULLABLE
nullable_dict['NO'] = NOT_NULLABLE


def create_column_def(table_def_dict: dict):

    column_def = []
    for key in table_def_dict.keys():
        column_def.append(
            TableDefinition.Column(
                key,
                sql_type_dict[table_def_dict[key]['type']],
                nullable_dict[table_def_dict[key]['nullable']])
            )

    return column_def


def create_hyper(
    dist_path: str,
    table_def_dict: dict,
    file_name: str,
    src_path: str
    ):
    # Hyperファイルを扱うためのセッションを作成
    with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
         with Connection(
             endpoint=hyper.endpoint,
             database=dist_path,
             create_mode=CreateMode.CREATE_AND_REPLACE
         ) as connection:

            column_def = create_column_def(table_def_dict)
            # テーブルを定義
            table_def = TableDefinition(
                table_name=file_name,
                columns=column_def
            )
            # テーブル定義をもとに仮想的にテーブル作成(default schemaはpublic)
            connection.catalog.create_table(table_def)
            # PostgreSQLライクにCOPYコマンドを実行
            record_count = connection.execute_command(
                command=f'''
                COPY {table_def.table_name} from {escape_string_literal(src_path)} with (format csv, delimiter ',', header)
                '''
            )
            print(f"The number of rows in table {table_def.table_name} is {record_count}.")


if __name__ == '__main__':

    input_dir = './input'
    table_def_dir = './table_def'
    dist_dir = './output'

    #フォルダ内のファイル名とフォルダ名をリストで出力
    input_file_name = [file_name[:-4] for file_name in os.listdir(input_dir) if '.csv' in file_name]
    #フォルダ内のファイル名とフォルダ名をリストで出力
    table_def_name = [file_name[:-5] for file_name in os.listdir(table_def_dir) if '.json' in file_name]

    # input/配下のファイルとtable_def/配下のファイル名が一致していることをチェック
    if set(input_file_name) != set(table_def_name):
        print('files in input directory do not coinside with those in table_def directory.')
        raise Exception

    # ファイルごとに処理
    for file_name in input_file_name:

        src_path = f'{os.path.join(input_dir, file_name)}.csv'
        dist_path = f'{os.path.join(dist_dir, file_name)}.hyper'
        table_def_path = f'{os.path.join(table_def_dir, file_name)}.json'
        with open(table_def_path) as f:
            table_def_dict = json.load(f)

        create_hyper(
            dist_path=dist_path,
            table_def_dict=table_def_dict,
            file_name=file_name,
            src_path=src_path
            )

    print('process completed.')
