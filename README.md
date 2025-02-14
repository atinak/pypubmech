# pypubmech

A Python package for fetching and processing PubMed articles with comprehensive metadata extraction and MeSH term support.

## Features

- Search PubMed articles by keyword or MeSH terms
- Extract comprehensive article metadata including:
  - Title, Abstract, Authors
  - Volume, Issue, Journal
  - Citations and Links
  - MeSH terms
- Export results to CSV
- Compare different sets of PMIDs

## Installation

```bash
pip install pypubmech
```

## Quick Start

```python
from pypubmech import PubMedClient

# Initialize client
client = PubMedClient(email="your.email@example.com")

# Search by keyword
pmids = client.search_by_keyword("cancer", 100)

# Fetch metadata
client.fetch_article_metadata()

# Export to CSV
client.export_to_csv("cancer_articles.csv")
```

## MeSH Search Example

```python
# Search using MeSH terms
mesh_query = "Neoplasms[MeSH] AND Genetics[MeSH]"
pmids = client.search_by_mesh(mesh_query)
client.fetch_article_metadata()
client.export_to_csv("cancer_genetics.csv")
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pypubmech.git
cd pypubmech
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.