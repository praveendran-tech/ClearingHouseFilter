#!/usr/bin/env python3
"""
Filter Clearinghouse student data (from CSV file) based on multiple
conditions and export only qualifying records to a new CSV.

INPUT:
    File:  ClearingHouse_2025.csv

OUTPUT:
    clearinghouse_filtered_output.csv

Current rules:

1. Include only rows where:
   - College Sequence > 1
   - Enrollment Status is NOT W or D

2. After all of that, discard any row where Graduated? == "Y".

(No date window enforced in this version.)
"""

import pandas as pd

# Column names from actual CSV
COL_FIRST_NAME       = "First Name"
COL_MIDDLE_NAME      = "Middle Initial"
COL_LAST_NAME        = "Last Name"
COL_REQUESTER_ID     = "Requester Return Field"
COL_COLLEGE_NAME     = "College Name"
COL_ENROLLMENT_MAJOR = "Enrollment Major 1"
COL_CLASS_LEVEL      = "Class Level"
COL_ENROLL_STATUS    = "Enrollment Status"
COL_ENROLL_DATE      = "Enrollment End"
COL_COLLEGE_SEQ      = "College Sequence"
COL_GRADUATED        = "Graduated?"

DEBUG = True   # set to False if you want less console output


def main():
    input_file = "ClearingHouse_2025.csv"
    print(f"Reading CSV: {input_file}")
    df = pd.read_csv(input_file, dtype=str)

    # Sanity check
    required_cols = [
        COL_FIRST_NAME, COL_MIDDLE_NAME, COL_LAST_NAME, COL_REQUESTER_ID,
        COL_COLLEGE_NAME, COL_ENROLLMENT_MAJOR, COL_CLASS_LEVEL,
        COL_ENROLL_STATUS, COL_ENROLL_DATE, COL_COLLEGE_SEQ, COL_GRADUATED
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    if DEBUG:
        print("Total rows:", len(df))

    # Normalize / parse
    df[COL_COLLEGE_SEQ] = pd.to_numeric(df[COL_COLLEGE_SEQ], errors="coerce")
    df["_status_norm"]  = df[COL_ENROLL_STATUS].str.upper().str.strip()
    df["_grad_norm"]    = df[COL_GRADUATED].str.upper().str.strip()

    # 1) Global filters: seq > 1 and status not W/D
    mask_seq_gt1 = df[COL_COLLEGE_SEQ] > 1
    mask_status  = ~df["_status_norm"].isin({"W", "D"})

    df_final = df[mask_seq_gt1 & mask_status].copy()

    if DEBUG:
        print("Rows after seq>1 & status filters:", len(df_final))

    # 2) Remove any rows with Graduated? = Y
    df_final = df_final[df_final[COL_GRADUATED].str.upper().str.strip() != "Y"]

    if DEBUG:
        print("Rows after removing Graduated=Y:", len(df_final))

    # Output columns
    output_cols = [
        COL_FIRST_NAME,
        COL_MIDDLE_NAME,
        COL_LAST_NAME,
        COL_REQUESTER_ID,
        COL_COLLEGE_NAME,
        COL_ENROLLMENT_MAJOR,
        COL_CLASS_LEVEL,
        COL_ENROLL_STATUS,
        COL_ENROLL_DATE,
        COL_COLLEGE_SEQ,
        COL_GRADUATED,
    ]

    df_final[output_cols].to_csv("clearinghouse_filtered_output.csv", index=False)
    print("✔ Output written → clearinghouse_filtered_output.csv")


if __name__ == "__main__":
    main()
