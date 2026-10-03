from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "supply_chain.csv"


def load_shipments():
    df = pd.read_csv(DATA_FILE)
    return df


def get_shipments():
    df = load_shipments()
    return df.to_dict(orient="records")


def get_shipment(shipment_id: str):
    df = load_shipments()

    result = df[
        df["shipment_id"].str.lower() == shipment_id.lower()
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()