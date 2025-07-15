# shason.py

import argparse
import sys
import fiona
import geopandas as gpd
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize rich console for beautiful printing
console = Console()

def list_layers_in_zip(zip_path: str) -> list:
    """
    Lists all vector layers available in a given ZIP archive.

    Args:
        zip_path: The file path to the .zip archive.

    Returns:
        A list of layer names found in the archive.
    """
    try:
        with fiona.open(f"zip://{zip_path}") as collection:
            layer_names = [layer for layer in collection.meta.get('layers', [])]
            # If fiona < 1.9, use listlayers for zip archives
            if not layer_names:
                layer_names = fiona.listlayers(f"zip://{zip_path}")
        return layer_names
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Could not read layers from '{zip_path}'.")
        console.print(f"Details: {e}")
        sys.exit(1)

def extract_layer_to_geojson(zip_path: str, layer_name: str) -> str:
    """
    Reads a specific layer from a ZIP archive and converts it to a GeoJSON string.

    Args:
        zip_path: The file path to the .zip archive.
        layer_name: The name of the layer to extract.

    Returns:
        A GeoJSON string representation of the layer.
    """
    try:
        console.print(f"\n[cyan]Reading layer[/cyan] '[bold yellow]{layer_name}[/bold yellow]'...")
        gdf = gpd.read_file(f"zip://{zip_path}", layer=layer_name)
        
        # Reproject to WGS 84 (EPSG:4326) if not already, as it's the standard for GeoJSON
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            console.print(f"[cyan]Reprojecting CRS from[/cyan] {gdf.crs.name} [cyan]to[/cyan] WGS 84 (EPSG:4326)...")
            gdf = gdf.to_crs(epsg=4326)

        console.print("[green]✔ Successfully read and processed the layer.[/green]")
        return gdf.to_json()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to extract layer '{layer_name}'.")
        console.print(f"Details: {e}")
        sys.exit(1)

def main():
    """Main function to run the interactive tool."""
    parser = argparse.ArgumentParser(
        description="An interactive tool to extract a Shapefile layer from a ZIP archive to GeoJSON."
    )
    parser.add_argument("zip_path", help="Path to the Shapefile ZIP archive.")
    args = parser.parse_args()

    console.print(Panel.fit(
        Text("Shapefile ZIP to GeoJSON Extractor", justify="center", style="bold magenta"),
        border_style="green"
    ))

    # 1. List available layers
    console.print(f"\n[cyan]Inspecting zip archive:[/cyan] [bold bright_blue]{args.zip_path}[/bold bright_blue]")
    layers = list_layers_in_zip(args.zip_path)
    if not layers:
        console.print("[bold red]Error:[/bold red] No vector layers found in the specified ZIP file.")
        sys.exit(1)

    # 2. Ask user to select a layer
    selected_layer = questionary.select(
        "Please select the layer you want to extract:",
        choices=layers,
        use_indicator=True,
        style=questionary.Style([('pointer', 'bold fg:yellow'), ('selected', 'fg:green')])
    ).ask()

    if not selected_layer:
        console.print("\n[yellow]No layer selected. Exiting.[/yellow]")
        sys.exit(0)

    # 3. Extract the selected layer to GeoJSON
    geojson_data = extract_layer_to_geojson(args.zip_path, selected_layer)

    # 4. Ask where to save the file
    default_filename = f"{selected_layer}.geojson"
    output_filename = questionary.text(
        "Enter the filename to save the GeoJSON:",
        default=default_filename
    ).ask()

    if not output_filename:
        console.print("\n[yellow]No output filename provided. Exiting.[/yellow]")
        sys.exit(0)

    try:
        with open(output_filename, "w") as f:
            f.write(geojson_data)
        console.print(Panel(
            f"✔ [bold green]Success![/bold green]\nLayer '[bold yellow]{selected_layer}[/bold yellow]' was saved to [bold bright_blue]{output_filename}[/bold bright_blue]",
            title="Export Complete",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Could not save file to '{output_filename}'.")
        console.print(f"Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
