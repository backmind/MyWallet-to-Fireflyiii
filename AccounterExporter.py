# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 21:56:45 2022

@author: backm
"""

import pandas as pd
import sqlite3

# CONFIG AREA
DB_PATH = "XX_XX_XXXX_ExpensoDB" # Full path to MyWallet Expense Manager database
OUTPUT_NAME = "dbexported.csv" # Full path of the exported csv database


# DEFINITION AREA

# Read sqlite into dict of pandas DataFrames
def read_sqlite(dbfile):
    with sqlite3.connect(dbfile) as dbcon:
        tables = list(pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';", dbcon)['name'])
        out = {tbl: pd.read_sql_query(
            f"SELECT * from {tbl}", dbcon) for tbl in tables}

    return out
# Query for an account, with fetching its initial founds.


def get_account(account):
        # Funtion to fetch each account in the database
    # Selecting only account
    df = pd_db[pd_db["acc_name"] == account]
    idd = acc[acc["acc_name"] == account].index

    
    # Fetching and appending initial founds
    date_init = df.exp_date.min()+pd.Timedelta(days=-1)
    amount_init = acc.loc[idd, "acc_initial"].values[0]
    exp_payee_name_init = "Initial founds"
    category_name_init = "Other"
    exp_note_init = "Initial founds"
    df = df.append(dict(zip(df.columns, [date_init, amount_init, exp_payee_name_init,
                   account, category_name_init, exp_note_init])), ignore_index=True)

    df.sort_values(by="exp_date", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_account_wtransfers(account):
    # This function gets the account but also all then transferences involving that account
    # Selecting only account
    df = pd_db[pd_db["acc_name"] == account]
    idd = acc[acc["acc_name"] == account].index
    dict_idnames = acc["acc_name"].to_dict()

    # Fetching and appending initial founds
    date_init = df.exp_date.min()+pd.Timedelta(days=-1)
    amount_init = acc.loc[idd, "acc_initial"].values[0]
    exp_payee_name_init = "Initial founds"
    category_name_init = "Other"
    exp_note_init = "Initial founds"
    df = df.append(dict(zip(df.columns, [date_init, amount_init, exp_payee_name_init,
                   account, category_name_init, exp_note_init])), ignore_index=True)

    # Feching and appending transferences
    # outcomming:
    out = transfer[transfer.trans_from_id.isin(
        idd)].reset_index(drop=True)
    out.trans_from_id.replace(dict_idnames, inplace=True)
    out.trans_to_id.replace(dict_idnames, inplace=True)
    out["trans_date"] = pd.to_datetime(out["trans_date"])
    out["trans_amount"] = out["trans_amount"]*-1
    out.rename(columns={"trans_date": "exp_date", "trans_amount": "exp_amount", "trans_note": "exp_note",
                'trans_from_id': "acc_name", 'trans_to_id': "exp_payee_name"}, inplace=True) 
    out["category_name"] = "Transfer"
    df = df.append(out)

    # incomming:
    inc = transfer[transfer.trans_to_id.isin(
        idd)].reset_index(drop=True)
    inc.trans_from_id.replace(dict_idnames, inplace=True)
    inc.trans_to_id.replace(dict_idnames, inplace=True)
    inc["trans_date"] = pd.to_datetime(inc["trans_date"])
    inc.rename(columns={"trans_date": "exp_date", "trans_amount": "exp_amount", "trans_note": "exp_note",
                'trans_from_id': "acc_name", 'trans_to_id': "exp_payee_name"}, inplace=True) 
    inc["category_name"] = "Transfer"
    df = df.append(inc)

    df.sort_values(by="exp_date", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# Load of all tables from database:

tbs = read_sqlite(DB_PATH)

tra = tbs["tbl_trans"].set_index("exp_id", drop=True)
acc = tbs["tbl_account"].set_index("acc_id", drop=True)
cat = tbs["tbl_cat"].set_index("category_id", drop=True)
transfer = tbs["tbl_transfer"].set_index("trans_id", drop=True)

pd_db = tra.merge(acc["acc_name"], left_on="exp_acc_id",
                  right_on="acc_id").drop(labels="exp_acc_id", axis=1)
pd_db = pd_db.merge(cat["category_name"], left_on="exp_cat",
                    right_on="category_id").drop(labels="exp_cat", axis=1)


# Only actual stuff, not programated one being not paid
pd_db = pd_db[pd_db.exp_is_paid == 1]
pd_db["exp_amount"] = pd_db.apply(
    lambda row: -row.exp_amount if row.exp_is_debit == 0 else row.exp_amount, axis=1)
pd_db["exp_date"] = pd.to_datetime(pd_db["exp_date"])
pd_db.sort_values(by="exp_date", ascending=True, inplace=True)
pd_db.reset_index(drop=True, inplace=True)


pd_db = pd_db[["exp_date", "exp_amount", "exp_payee_name",
               "acc_name", "category_name", "exp_note"]]


# Populating a dataframe with all accounts data
df_acc = pd.DataFrame()

for acc_name in acc["acc_name"]:
    df_acc = df_acc.append(get_account(acc_name))
    
    
# Feching and appending transferences
dict_idnames = acc["acc_name"].to_dict()
df_trn = transfer.reset_index(drop=True)
df_trn.trans_from_id.replace(dict_idnames, inplace=True)
df_trn.trans_to_id.replace(dict_idnames, inplace=True)
df_trn["trans_date"] = pd.to_datetime(df_trn["trans_date"])
df_trn["trans_amount"] = df_trn["trans_amount"]*-1
df_trn.rename(columns={"trans_date": "exp_date", "trans_amount": "exp_amount", "trans_note": "exp_note",
            'trans_from_id': "acc_name", 'trans_to_id': "exp_payee_name"}, inplace=True)    
df_trn["category_name"] = "Transfer"
df_acc = df_acc.append(df_trn)  

#trimming multiline notes
df_acc["exp_note"] = df_acc["exp_note"].str.replace(
    '\r', ' ').replace('\n', ' ').str.strip()

# Shorting and reindexing dataframe
df_acc.sort_values(by="exp_date", ascending=True, inplace=True)
df_acc.reset_index(drop=True, inplace=True)

# Exporting csv
df_acc.to_csv(OUTPUT_NAME, sep="\t")
