# hook-geopandas.py
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('pyproj')
datas += collect_data_files('shapely')