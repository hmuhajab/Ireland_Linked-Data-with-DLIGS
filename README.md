# Ireland_Linked-Data-with-DLIGS



# Ireland Geographic Data Preparation

## Project Overview

This repository contains the necessary scripts and ontology files for preprocessing, cleansing, and organizing geographic data related to Ireland. The Jupyter notebook `preparation_data.ipynb` is designed to transform raw data into an analysis-ready forma. Additionally, scripts in the `Scripts` folder utilize the ontology in the `ontology` folder to populate data models, preparing them for integration into geographic information systems.




## Features

- **Data extraction** from multiple geographic data sources.
- **Cleansing and normalization** of geographic data.
- **Integration of data** into a unified dligs schema.
- **Ontology-based data population** using RDF and OWL standards.

## Data Normalization Techniques

Normalization techniques in this project ensure data consistency and suitability for GIS applications:

- **Encoding Normalization:** Detect and set the correct encoding for CSV file imports using the `chardet` library.
- **Whitespace Normalization:** Remove or replace unnecessary spaces within strings, e.g., replacing spaces with underscores in names to avoid URL encoding issues.
- **Deduplication:** Remove duplicate entries using `df.drop_duplicates()` to ensure data uniqueness.
- **Data Type Normalization:** Standardize data formats, such as converting all dates to a consistent format or ensuring numerical data adheres to specified formats.

## Scripts Overview

The scripts within the `Scripts` folder perform the following operations:

- **Ontology Loading and Instance Creation:** Scripts load the ontology framework and create instances based on the geographic data extracted and cleansed in the preprocessing steps.
- **Data Populating:** Utilize the ontology to systematically populate the geographic data into structured formats that adhere to the ontology's schema.


## Ontology Folder

The `ontology` folder contains RDF and OWL files that define the structure and relationships of geographic entities. These ontologies are crucial for the semantic organization of geographic data, enabling complex queries and data interlinking within GIS applications.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Required Python libraries: `pandas`, `numpy`, `geopandas`

You can install the necessary libraries using pip:

```bash
pip install notebook pandas numpy geopandas

