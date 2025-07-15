# tests/test_shason.py

import pytest
import os
import zipfile
import json
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Import the main function from your script
from shason import main

@pytest.fixture
def create_test_shapefile_zip(tmp_path):
    """
    A pytest fixture to create a temporary, valid Shapefile ZIP archive for testing.
    This fixture creates a zip file with two layers: one with points, one with polygons.
    This makes our test self-contained and reliable.
    """
    # Create a temporary directory for shapefile components
    shapefile_dir = tmp_path / "shapefile_source"
    shapefile_dir.mkdir()
    
    # 1. Create Point Layer in EPSG:4326
    point_gdf = gpd.GeoDataFrame(
        {'id': [1], 'name': ['test_point']},
        geometry=[Point(10, 50)],
        crs="EPSG:4326"
    )
    point_shp_path = shapefile_dir / "points_layer.shp"
    point_gdf.to_file(point_shp_path)

    # 2. Create Polygon Layer in a different CRS to test reprojection
    poly_gdf = gpd.GeoDataFrame(
        {'id': [1], 'area': [100]},
        geometry=[Polygon([(0,0), (1,1), (1,0), (0,0)])],
        crs="EPSG:3857"
    )
    poly_shp_path = shapefile_dir / "polygons_layer.shp"
    poly_gdf.to_file(poly_shp_path)

    # 3. Zip all the created files into a single archive
    zip_path = tmp_path / "test_shapefile.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file in shapefile_dir.iterdir():
            zf.write(file, arcname=file.name)
            
    return zip_path

def test_full_end_to_end_success(mocker, create_test_shapefile_zip, tmp_path):
    """
    Tests the successful end-to-end flow:
    - Runs the script with the temporary zip file.
    - Simulates the user selecting the 'polygons_layer'.
    - Simulates the user accepting the default output filename.
    - Verifies the output GeoJSON file is correct.
    """
    test_zip_path = create_test_shapefile_zip
    selected_layer_name = "polygons_layer"
    output_filename = f"{selected_layer_name}.geojson"
    output_filepath = tmp_path / output_filename

    # Change current working directory to the temporary one, so the output file is saved there
    os.chdir(tmp_path)

    # Mock command-line arguments and all interactive user prompts
    mocker.patch("sys.argv", ["shason.py", str(test_zip_path)])
    mocker.patch("questionary.select").return_value.ask.return_value = selected_layer_name
    mocker.patch("questionary.text").return_value.ask.return_value = output_filename

    # Run the main application
    main()

    # --- Assertions ---
    # 1. Check if the output GeoJSON file was actually created
    assert output_filepath.exists(), "The output GeoJSON file was not created."

    # 2. Check the content of the created GeoJSON file
    with open(output_filepath, 'r') as f:
        geojson_data = json.load(f)

    assert geojson_data['type'] == "FeatureCollection"
    assert len(geojson_data['features']) == 1
    
    feature = geojson_data['features'][0]
    assert feature['geometry']['type'] == "Polygon"
    assert feature['properties']['area'] == 100
    
    # 3. Verify the Coordinate Reference System (CRS) was reprojected to WGS 84
    output_gdf = gpd.read_file(output_filepath)
    assert output_gdf.crs.to_epsg() == 4326