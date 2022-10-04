import argparse

import pandas as pd


def reformat_vehicle_data(input: str, output: str) -> None:
    """Reformat vehicle data from input file to output file.

    Args:
        input (str): Path to input file.
        output (str): Path to output file.
    """
    # Use postcode row as headers, skip the other header row
    df = pd.read_csv(input, header=9, skiprows=[10])

    # Manually add in other headers
    df = df.rename(
        columns={
            "Unnamed: 0": "Make/Model",
            "Unnamed: 1": "Year of manufacture",
            "Aust Postcode": "Fuel type",
        }
    )

    # Drop annotations columns
    df = df.loc[:, ~df.columns.str.endswith(" - Annotations")]

    # forward fill Make/Model
    df["Make/Model"] = df["Make/Model"].fillna(method="ffill")

    # Make postcodes into columns
    df = df.melt(
        id_vars=["Make/Model", "Year of manufacture", "Fuel type"],
        var_name="Postcode",
        value_name="Count",
    )

    # Drop rows with no count
    df = df[df["Count"] > 0]

    # Reorder columns
    df = df[["Postcode", "Make/Model", "Year of manufacture", "Fuel type", "Count"]]

    # Write to file
    df.to_csv(output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reformat ABS Postcode Vehicle Data.")
    parser.add_argument(
        "input", help="The input CSV file", default="input.csv", nargs="?"
    )
    parser.add_argument(
        "--output", help="The output CSV file", default="output.csv", nargs="?"
    )
    args = parser.parse_args()
    reformat_vehicle_data(args.input, args.output)
