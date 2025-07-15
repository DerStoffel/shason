SHASON
--------------------------------------------------------------------------------

# Shapefile ZIP to GeoJSON Extractor

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)

A user-friendly, interactive command-line tool to inspect a zipped Shapefile, select a specific layer, and export it as a GeoJSON file. The tool automatically handles reading from the `.zip` archive and reprojects the data to WGS 84 (EPSG:4326) for standardized GeoJSON output.

## Key Features

-   **Direct ZIP Reading**: No need to manually unzip your Shapefiles. The tool reads directly from the `.zip` archive.
-   **Interactive Layer Selection**: Automatically lists all available vector layers and provides a clean, interactive prompt for you to choose one.
-   **GeoJSON Export**: Converts the selected layer to GeoJSON, the web standard for geographic data.
-   **CRS Reprojection**: Automatically reprojects data to WGS 84 (EPSG:4326) for maximum compatibility.
-   **User-Friendly CLI**: Uses colored output and clear prompts for a smooth user experience.
-   **Self-Contained**: A single Python script with a few common dependencies.

## Demo

Here is an example of the interactive session:

![Screenshot of the interactive tool in action, showing colored text and prompts for layer selection and filename input.](https://i.imgur.com/GjT8l0R.png)

## Installation

To use this tool, you need Python 3.8+ installed. It's highly recommended to use a virtual environment.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install geopandas fiona questionary rich
    ```

## Usage

Run the script from your terminal and provide the path to your zipped Shapefile as the only argument.

```bash
python shptool.py /path/to/your/shapefile.zip
