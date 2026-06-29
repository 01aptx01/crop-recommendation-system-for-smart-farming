from __future__ import annotations

import hashlib
import json
import warnings
from pathlib import Path
from typing import Any, Optional

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "raw" / "pre-combine"
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "central"
OUTPUT_PATH = OUTPUT_DIR / "central_raw_dataset.csv"
SUMMARY_PATH = OUTPUT_DIR / "central_raw_dataset_summary.csv"
UNIT_DICTIONARY_PATH = OUTPUT_DIR / "central_unit_dictionary.csv"
REQUIRED_FEATURES_PATH = OUTPUT_DIR / "central_required_features_raw.csv"
REQUIRED_FEATURES_SUMMARY_PATH = OUTPUT_DIR / "central_required_features_summary.csv"


# Keep units as metadata instead of converting values. This prevents rows from
# different sources being silently mixed under incompatible assumptions.
SOURCE_UNITS: dict[str, dict[str, str]] = {
    "crop-yield.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "ph": "pH",
        "humidity": "%",
        "soil_moisture": "%",
        "temperature": "degC",
        "rainfall": "mm/year",
        "area": "unknown",
        "fertilizer": "unknown_numeric",
        "pesticide": "unknown_numeric",
        "yield": "unknown",
    },
    "data_core.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "humidity": "%",
        "soil_moisture": "%",
        "temperature": "degC",
        "fertilizer": "categorical",
    },
    "Crop_Recommendation.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "ph": "pH",
        "humidity": "%",
        "temperature": "degC",
        "rainfall": "unknown_low_scale_not_converted",
    },
    "Crop_recommendation-3.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "ph": "pH",
        "humidity": "%",
        "temperature": "degC",
        "rainfall": "unknown_low_scale_not_converted",
    },
    "crop_yield.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "ph": "pH",
        "humidity": "%",
        "temperature": "degC",
        "rainfall": "mm/year",
        "area": "unknown",
        "fertilizer": "unknown_numeric",
        "pesticide": "unknown_numeric",
        "production": "unknown",
        "yield": "unknown",
    },
    "crop_data.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "ph": "pH",
        "temperature": "degC",
        "rainfall": "mm/year",
    },
    "Crop and fertilizer dataset.csv": {
        "n": "kg/ha",
        "p": "kg/ha",
        "k": "kg/ha",
        "ph": "pH",
        "temperature": "degC",
        "rainfall": "mm/year",
        "fertilizer": "categorical",
    },
    "Crop Recommendation using Soil Properties and Weather Prediction.csv": {
        "n": "%",
        "p": "ppm",
        "k": "ppm",
        "ph": "pH",
        "soil_moisture": "fraction_0_1",
        "Zinc": "ppm",
        "Sulfur": "ppm",
        "Humidity_Winter": "%",
        "Humidity_Spring": "%",
        "Humidity_Summer": "%",
        "Humidity_Autumn": "%",
        "Max_Temp_Winter": "degC",
        "Max_Temp_Spring": "degC",
        "Max_Temp_Summer": "degC",
        "Max_Temp_Autumn": "degC",
        "Min_Temp_Winter": "degC",
        "Min_Temp_Spring": "degC",
        "Min_Temp_Summer": "degC",
        "Min_Temp_Autumn": "degC",
        "Precipitation_Winter": "unknown",
        "Precipitation_Spring": "unknown",
        "Precipitation_Summer": "unknown",
        "Precipitation_Autumn": "unknown",
    },
    "original_dataset.csv": {
        "n": "kg/ha_assumed_from_source_family",
        "p": "kg/ha_assumed_from_source_family",
        "k": "kg/ha_assumed_from_source_family",
        "ph": "pH",
        "humidity": "%",
        "temperature": "degC",
        "rainfall": "unknown_low_scale_not_converted",
    },
}


SOURCE_NOTES: dict[str, str] = {
    "Crop_Recommendation.csv": (
        "Rainfall max is below 300 in this source; kept as raw low-scale rainfall "
        "and not converted to yearly millimeters."
    ),
    "Crop_recommendation-3.csv": (
        "Rainfall max is below 300 in this source; kept as raw low-scale rainfall "
        "and not converted to yearly millimeters."
    ),
    "Crop Recommendation using Soil Properties and Weather Prediction.csv": (
        "N is percent; P and K are ppm. Weather features are seasonal, so canonical "
        "temperature/rainfall are left blank and original columns are preserved."
    ),
    "original_dataset.csv": (
        "Rainfall max is below 300 and unit was not provided in the prompt; kept "
        "unconverted."
    ),
}


CANONICAL_VALUE_COLUMNS = [
    "label",
    "area",
    "soil_type",
    "soil_color",
    "ph",
    "n",
    "p",
    "k",
    "humidity",
    "soil_moisture",
    "temperature",
    "rainfall",
    "state",
    "year",
    "season",
    "district_name",
    "region",
    "production",
    "yield",
    "fertilizer",
    "pesticide",
]

UNIT_COLUMNS = [
    "area_unit",
    "ph_unit",
    "n_unit",
    "p_unit",
    "k_unit",
    "humidity_unit",
    "soil_moisture_unit",
    "temperature_unit",
    "rainfall_unit",
    "production_unit",
    "yield_unit",
    "fertilizer_unit",
    "pesticide_unit",
]

META_COLUMNS = [
    "central_raw_id",
    "source_file",
    "source_path",
    "source_row_id",
    "source_record_hash",
    "source_note",
]


def read_table(path: Path) -> pd.DataFrame:
    last_error: Optional[Exception] = None
    for encoding in ("utf-8", "utf-8-sig", "latin1"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Could not read {path}")


def hash_record(record: dict[str, Any]) -> str:
    payload = json.dumps(record, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def make_blank_series(df: pd.DataFrame) -> pd.Series:
    return pd.Series([pd.NA] * len(df), index=df.index)


def add_if_present(out: pd.DataFrame, df: pd.DataFrame, column: str) -> None:
    out[column] = df[column] if column in df.columns else make_blank_series(df)


def add_unit(out: pd.DataFrame, df: pd.DataFrame, source_file: str, value_col: str) -> None:
    unit_col = f"{value_col}_unit"
    if unit_col not in UNIT_COLUMNS:
        return
    source_units = SOURCE_UNITS.get(source_file, {})
    if value_col in df.columns and value_col in source_units:
        out[unit_col] = source_units[value_col]
    else:
        out[unit_col] = pd.NA


def build_one(path: Path, central_id_start: int) -> pd.DataFrame:
    df = read_table(path)
    source_file = path.name
    source_path = path.relative_to(PROJECT_ROOT).as_posix()

    out = pd.DataFrame(index=df.index)
    out["central_raw_id"] = [f"CRAW-{i:06d}" for i in range(central_id_start, central_id_start + len(df))]
    out["source_file"] = source_file
    out["source_path"] = source_path
    out["source_row_id"] = range(1, len(df) + 1)
    out["source_record_hash"] = [hash_record(row) for row in df.to_dict(orient="records")]
    out["source_note"] = SOURCE_NOTES.get(source_file, "")

    for column in CANONICAL_VALUE_COLUMNS:
        add_if_present(out, df, column)

    for column in UNIT_COLUMNS:
        out[column] = pd.NA

    for value_col in [
        "area",
        "ph",
        "n",
        "p",
        "k",
        "humidity",
        "soil_moisture",
        "temperature",
        "rainfall",
        "production",
        "yield",
        "fertilizer",
        "pesticide",
    ]:
        add_unit(out, df, source_file, value_col)

    raw_df = df.add_prefix("raw__")
    return pd.concat([out, raw_df], axis=1)


def build_unit_dictionary(paths: list[Path]) -> pd.DataFrame:
    rows = []
    for path in paths:
        df = read_table(path)
        source_units = SOURCE_UNITS.get(path.name, {})
        for column in df.columns:
            rows.append(
                {
                    "source_file": path.name,
                    "source_column": column,
                    "unit": source_units.get(column, "not_specified"),
                    "mapped_to_central_column": column if column in CANONICAL_VALUE_COLUMNS else "",
                    "note": SOURCE_NOTES.get(path.name, ""),
                }
            )
    return pd.DataFrame(rows)


def build_summary(central: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for source_file, group in central.groupby("source_file", sort=True):
        row = {
            "source_file": source_file,
            "rows": len(group),
            "source_note": group["source_note"].dropna().iloc[0] if len(group) else "",
        }
        for column in CANONICAL_VALUE_COLUMNS:
            row[f"{column}_non_null"] = int(group[column].notna().sum())
        for column in ["n_unit", "p_unit", "k_unit", "rainfall_unit"]:
            row[column] = "; ".join(sorted(map(str, group[column].dropna().unique())))
        rows.append(row)
    return pd.DataFrame(rows)


def build_required_features(central: pd.DataFrame) -> pd.DataFrame:
    required = pd.DataFrame(
        {
            "central_feature_id": central["central_raw_id"].str.replace("CRAW", "CFEAT", regex=False),
            "source_file": central["source_file"],
            "source_path": central["source_path"],
            "source_row_id": central["source_row_id"],
            "source_record_hash": central["source_record_hash"],
            "source_note": central["source_note"],
            "label": central["label"],
            "area_size": central["area"],
            "area_size_unit": central["area_unit"],
            "soil_type": central["soil_type"],
            "ph": central["ph"],
            "ph_unit": central["ph_unit"],
            "n": central["n"],
            "n_unit": central["n_unit"],
            "p": central["p"],
            "p_unit": central["p_unit"],
            "k": central["k"],
            "k_unit": central["k_unit"],
            "soil_humidity": central["soil_moisture"],
            "soil_humidity_unit": central["soil_moisture_unit"],
            "temp": central["temperature"],
            "temp_unit": central["temperature_unit"],
            "rainfall": central["rainfall"],
            "rainfall_unit": central["rainfall_unit"],
        }
    )

    feature_groups = {
        "area_size": ["area_size"],
        "soil_type": ["soil_type"],
        "ph": ["ph"],
        "npk": ["n", "p", "k"],
        "soil_humidity": ["soil_humidity"],
        "temp": ["temp"],
        "rainfall": ["rainfall"],
    }

    for feature_name, columns in feature_groups.items():
        required[f"has_{feature_name}"] = required[columns].notna().all(axis=1)

    feature_flags = [f"has_{name}" for name in feature_groups]
    required["required_feature_count"] = required[feature_flags].sum(axis=1).astype(int)
    required["is_required_feature_complete"] = required[feature_flags].all(axis=1)

    missing_values = []
    for _, row in required.iterrows():
        missing = [name for name in feature_groups if not bool(row[f"has_{name}"])]
        missing_values.append(";".join(missing))
    required["missing_required_features"] = missing_values

    return required


def build_required_features_summary(required: pd.DataFrame) -> pd.DataFrame:
    feature_flags = [
        "has_area_size",
        "has_soil_type",
        "has_ph",
        "has_npk",
        "has_soil_humidity",
        "has_temp",
        "has_rainfall",
    ]
    rows = []
    for source_file, group in required.groupby("source_file", sort=True):
        row = {
            "source_file": source_file,
            "rows": len(group),
            "complete_required_rows": int(group["is_required_feature_complete"].sum()),
            "avg_required_feature_count": round(float(group["required_feature_count"].mean()), 4),
        }
        for flag in feature_flags:
            row[f"{flag}_rows"] = int(group[flag].sum())
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

    paths = sorted(INPUT_DIR.glob("*.csv"))
    if not paths:
        raise FileNotFoundError(f"No CSV files found in {INPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = []
    next_id = 1
    for path in paths:
        frame = build_one(path, next_id)
        frames.append(frame)
        next_id += len(frame)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        central = pd.concat(frames, ignore_index=True, sort=False)
    ordered_columns = META_COLUMNS + CANONICAL_VALUE_COLUMNS + UNIT_COLUMNS
    raw_columns = sorted([c for c in central.columns if c.startswith("raw__")])
    central = central[ordered_columns + raw_columns]

    central.to_csv(OUTPUT_PATH, index=False)
    build_summary(central).to_csv(SUMMARY_PATH, index=False)
    build_unit_dictionary(paths).to_csv(UNIT_DICTIONARY_PATH, index=False)
    required = build_required_features(central)
    required.to_csv(REQUIRED_FEATURES_PATH, index=False)
    build_required_features_summary(required).to_csv(REQUIRED_FEATURES_SUMMARY_PATH, index=False)

    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Rows: {len(central):,}")
    print(f"Columns: {len(central.columns):,}")
    print(f"Wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {UNIT_DICTIONARY_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REQUIRED_FEATURES_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REQUIRED_FEATURES_SUMMARY_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
