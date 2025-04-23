import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path


def parse_indices(input_str, max_index):
    """Parse a string like '1,3,5-8,10' into a sorted list of unique indices."""
    indices = set()
    tokens = [token.strip() for token in input_str.split(",")]
    for token in tokens:
        if "-" in token:
            start, end = token.split("-")
            try:
                start = int(start)
                end = int(end)
                if start > end:
                    start, end = end, start
                for i in range(start, end + 1):
                    if 0 <= i < max_index:
                        indices.add(i)
            except ValueError:
                continue
        else:
            try:
                idx = int(token)
                if 0 <= idx < max_index:
                    indices.add(idx)
            except ValueError:
                continue
    return sorted(indices)


def get_parquet_links(url, dataset_type="all"):
    """Finds all Parquet file links on a given webpage, filtered by dataset type."""
    try:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()  # Remove leading/trailing spaces
            if href.lower().endswith(".parquet"):  # Case-insensitive check
                href_lower = href.lower()
                # Filter by dataset type
                if dataset_type == "yellow" and "yellow" not in href_lower:
                    continue
                if dataset_type == "green" and "green" not in href_lower:
                    continue
                if dataset_type == "fhv" and "fhv" not in href_lower:
                    continue
                if dataset_type == "fhvhv" and "fhvhv" not in href_lower:
                    continue
                absolute_url = urljoin(url, href)
                links.append(absolute_url)
        return links
    except httpx.RequestError as e:
        print(f"Error fetching URL: {e}")
        return []


def download_files(links, download_dir="seeds"):
    """Downloads files from the given URLs to the specified directory, skipping existing files."""
    download_dir = Path(download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    for link in links:
        filename = Path(link).name
        filepath = download_dir / filename
        if filepath.exists():
            print(f"Skipping {filename}: already exists.")
            continue
        try:
            print(f"Downloading {link} to {filepath}")
            with httpx.stream("GET", link, follow_redirects=True) as response:
                response.raise_for_status()
                with filepath.open("wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
            print(f"Downloaded {filename} successfully.")
        except httpx.RequestError as e:
            print(f"Failed to download {link}: {e}")


if __name__ == "__main__":
    tlc_trip_data_url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    print("Which dataset do you want to download?")
    print("[y]ellow, [g]reen, [f]hv, [h]igh volume fhv, [a]ll")
    dataset_choice = input("Enter your choice (y/g/f/h/a): ").strip().lower()
    if dataset_choice == "y":
        dataset_type = "yellow"
    elif dataset_choice == "g":
        dataset_type = "green"
    elif dataset_choice == "f":
        dataset_type = "fhv"
    elif dataset_choice == "h":
        dataset_type = "fhvhv"
    else:
        dataset_type = "all"

    parquet_links = get_parquet_links(tlc_trip_data_url, dataset_type)

    if parquet_links:
        print("\nFound Parquet files:")
        for i, link in enumerate(parquet_links):
            print(f"[{i}] {link}")

        selected_indices = input(
            "\nEnter the indices (e.g., 0,1,2 or 13-24), 'all', or a 4-digit year (e.g., 2023): "
        ).strip()

        # Check for 4-digit year
        if selected_indices.lower() == "all":
            download_links = parquet_links
        elif selected_indices.isdigit() and len(selected_indices) == 4:
            year = selected_indices
            download_links = [link for link in parquet_links if year in Path(link).name]
            if not download_links:
                print(f"No files found for year {year}.")
        else:
            indices = parse_indices(selected_indices, len(parquet_links))
            download_links = [parquet_links[i] for i in indices]

        if download_links:
            download_files(download_links)
        else:
            print("No files selected for download.")
    else:
        print("No Parquet files found on the page.")
