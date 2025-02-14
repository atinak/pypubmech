"""
pypubmech - A Python package for fetching and processing PubMed articles
with support for MeSH terms and comprehensive metadata extraction.
"""

import pandas as pd
from metapub import PubMedFetcher
from Bio import Entrez
from tqdm import tqdm
from typing import List, Dict, Set, Optional
from functools import reduce


class PubMedClient:
    """
    A client for fetching and processing articles from PubMed using both MetaPub and Entrez APIs.
    Supports comprehensive metadata extraction including volumes, issues, journals, and citations.
    """
    
    def __init__(self, email: str):
        """
        Initialize the PubMedClient with necessary configurations.
        
        Args:
            email (str): Email address for Entrez API authentication
        """
        self.fetch = PubMedFetcher()
        Entrez.email = email
        self.pmids = []
        self.article_data = {
            'titles': {}, 'abstracts': {}, 'authors': {},
            'years': {}, 'mesh': {}, 'links': {},
            'volumes': {}, 'issues': {}, 'journals': {},
            'citations': {}
        }
        
    def search_by_keyword(self, keyword: str, num_articles: int = 100) -> List[str]:
        """
        Search PubMed articles by keyword.
        
        Args:
            keyword (str): Search term
            num_articles (int): Maximum number of articles to retrieve
            
        Returns:
            List[str]: List of PMIDs
        """
        self.pmids = self.fetch.pmids_for_query(keyword, retmax=num_articles)
        return self.pmids
    
    def search_by_mesh(self, mesh_query: str, max_results: int = 10000) -> List[str]:
        """
        Search PubMed articles using MeSH terms.
        
        Args:
            mesh_query (str): MeSH query string
            max_results (int): Maximum number of results to retrieve
            
        Returns:
            List[str]: List of PMIDs
        """
        try:
            handle = Entrez.esearch(db='pubmed', term=mesh_query, retmax=max_results)
            record = Entrez.read(handle)
            self.pmids = record['IdList']
            return self.pmids
        except Exception as e:
            print(f"Error in MeSH search: {str(e)}")
            return []

    def fetch_article_metadata(self, pmids: Optional[List[str]] = None) -> None:
        """
        Fetch comprehensive metadata for articles based on PMIDs.
        
        Args:
            pmids (List[str], optional): List of PMIDs to process. If None, uses stored PMIDs.
        """
        if pmids is None:
            pmids = self.pmids
            
        for pmid in tqdm(pmids, desc="Fetching articles"):
            try:
                article = self.fetch.article_by_pmid(pmid)
                
                # Store basic metadata
                self.article_data['titles'][pmid] = article.title
                self.article_data['abstracts'][pmid] = article.abstract
                self.article_data['authors'][pmid] = article.authors
                self.article_data['years'][pmid] = article.year
                self.article_data['links'][pmid] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                
                # Store additional metadata
                self.article_data['volumes'][pmid] = article.volume
                self.article_data['issues'][pmid] = article.issue
                self.article_data['journals'][pmid] = article.journal
                self.article_data['citations'][pmid] = article.citation
                
                # Process MeSH terms if available
                mesh_dict = article.mesh
                if mesh_dict:
                    self.article_data['mesh'][pmid] = [
                        value['descriptor_name'] for value in mesh_dict.values()
                    ]
            except Exception as e:
                print(f"Error processing PMID {pmid}: {str(e)}")
                continue
    
    def create_dataframe(self) -> pd.DataFrame:
        """
        Create a pandas DataFrame from collected article metadata.
        
        Returns:
            pd.DataFrame: Combined DataFrame with all article metadata
        """
        # Create individual DataFrames for each data type
        dataframes = []
        column_names = {
            'titles': 'Title',
            'abstracts': 'Abstract',
            'authors': 'Author',
            'years': 'Year',
            'mesh': 'MeSH',
            'links': 'Link',
            'volumes': 'Volume',
            'issues': 'Issue',
            'journals': 'Journal',
            'citations': 'Citation'
        }
        
        for key, name in column_names.items():
            if self.article_data[key]:
                df = pd.DataFrame(
                    list(self.article_data[key].items()),
                    columns=['pmid', name]
                )
                dataframes.append(df)
        
        # Merge all DataFrames
        if dataframes:
            return reduce(
                lambda left, right: pd.merge(
                    left, right, on=['pmid'], how='outer'
                ),
                dataframes
            )
        return pd.DataFrame()
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export the collected data to a CSV file.
        
        Args:
            filename (str): Name of the output CSV file
        """
        df = self.create_dataframe()
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
    
    @staticmethod
    def find_uncommon_pmids(set1: Set[str], set2: Set[str]) -> Set[str]:
        """
        Find PMIDs that are unique to either set.
        
        Args:
            set1 (Set[str]): First set of PMIDs
            set2 (Set[str]): Second set of PMIDs
            
        Returns:
            Set[str]: PMIDs that appear in only one of the sets
        """
        return set1.symmetric_difference(set2)