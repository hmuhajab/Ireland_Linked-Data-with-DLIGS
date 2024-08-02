# Ireland_Linked-Data-with-DLIGS

# Ireland Geographic Data Preparation Folder

## Project Overview

This repository contains the Jupyter notebook `preparation_data.ipynb`, which is designed to preprocess and organize geographic data related to Ireland. The notebook outlines a structured approach to transform raw data into an analysis-ready format.

## Features

- Data extraction from multiple geographic data sources.
- Cleansing and normalization of geographic data.
- Integration of data into a unified schema suitable for GIS applications.

## Data Normalization Techniques

The preprocessing of geographic data in this project involves normalization techniques to ensure the data is consistent and suitable for population into the DLIGS model.

- **Encoding Normalization**: The `chardet` library is used to detect and set the correct encoding for CSV file imports, ensuring that all characters in the data are interpreted correctly. This step is crucial to prevent issues related to character misrepresentation, especially with non-standard characters.

- **Whitespace Normalization**: The data undergoes various cleaning operations to remove or replace unnecessary spaces within strings. For example, spaces are replaced with underscores in name fields to prevent issues during URL encoding (e.g., spaces turning into `%20` in web contexts).

- **Deduplication**: Duplicate entries within the dataset are identified and removed using the `df.drop_duplicates()` function. This process helps maintain a clean dataset by ensuring that each entry is unique.




## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- Required Python libraries: `pandas`, `numpy`, `geopandas`

You can install the necessary libraries using pip:

```bash
pip install notebook pandas numpy geopandas
