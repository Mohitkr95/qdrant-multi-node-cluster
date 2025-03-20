"""
Main class for the Qdrant cluster demonstration.
"""

import logging
import time
from typing import List, Dict, Any, Optional, Tuple
import json
from rich.console import Console
from rich.logging import RichHandler

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models

from qdrant_demo.config import settings
from qdrant_demo.utils import data_generator


# Set up rich logging
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)


class QdrantClusterDemo:
    """
    A class to demonstrate Qdrant vector database capabilities in a multi-node cluster setup.
    """
    
    def __init__(self, host: str = settings.QDRANT_HOST, port: int = settings.QDRANT_PORT):
        """
        Initialize the Qdrant cluster demo.
        
        Args:
            host: Hostname for the Qdrant server
            port: Port for the Qdrant server
        """
        # Configure logging
        self.logger = logging.getLogger("qdrant_demo")
        self.console = Console()
        logging.getLogger("httpx").setLevel(logging.WARNING)
        
        # Initialize client
        self.client = QdrantClient(host, port=port)
        self.collection_name = settings.COLLECTION_NAME
        self.shard_key = settings.SHARD_KEY
        self.vector_size = settings.VECTOR_SIZE
    
    def _log_section(self, title):
        """Log a section header with a divider."""
        self.console.print(f"\n[bold cyan]{'='*50}[/bold cyan]")
        self.console.print(f"[bold cyan]{title.center(50)}[/bold cyan]")
        self.console.print(f"[bold cyan]{'='*50}[/bold cyan]\n")
    
    def _format_response(self, response):
        """Format a response for cleaner logging."""
        if hasattr(response, '__dict__'):
            return str(response)
        return str(response)
    
    def setup_collection(self) -> None:
        """Set up a collection with advanced configuration including sharding and replication."""
        self._log_section("COLLECTION SETUP")
        
        # Delete existing collection if it exists
        response = self.client.delete_collection(collection_name=self.collection_name)
        self.logger.info(f"Collection '{self.collection_name}' deleted: [bold]{'Success' if response else 'Not found'}[/bold]")
        
        # Create new collection with specific configuration
        response = self.client.create_collection(
            collection_name=self.collection_name,
            shard_number=settings.SHARD_NUMBER,
            vectors_config=models.VectorParams(
                size=self.vector_size, 
                distance=models.Distance.COSINE
            ),
            optimizers_config=models.OptimizersConfigDiff(
                indexing_threshold=20000,
                memmap_threshold=50000
            ),
            on_disk_payload=True
        )
        self.logger.info(f"Collection created with custom sharding: [bold green]{'Success' if response else 'Failed'}[/bold green]")
        
        # Create field index for payload filtering
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="category",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        self.logger.info(f"Payload index created for 'category' field: [bold green]Success[/bold green]")
    
    def insert_data(self, count: int = settings.DEFAULT_POINT_COUNT) -> None:
        """
        Insert a specified number of random vectors with payload.
        
        Args:
            count: Number of vector points to insert
        """
        self._log_section("DATA INSERTION")
        
        progress_interval = count // 10  # Show progress 10 times
        self.console.print(f"[yellow]Inserting {count} vectors into collection...[/yellow]")
        
        point_counter = 0
        start_time = time.time()
        
        for _ in range(count):
            random_vector = data_generator.generate_random_vector(self.vector_size)
            point_counter += 1
            payload = data_generator.generate_payload()
            
            response = self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=point_counter,
                        vector=random_vector,
                        payload=payload
                    ),
                ],
            )
            if point_counter % progress_interval == 0 or point_counter == count:
                progress_pct = int(point_counter / count * 100)
                self.console.print(f"[yellow]Progress: [bold]{progress_pct}%[/bold] ({point_counter}/{count})[/yellow]")
                
        elapsed_time = time.time() - start_time
        self.console.print(f"[bold green]Completed insertion of {count} points in {elapsed_time:.2f} seconds![/bold green]")
    
    def demonstrate_vector_search(self) -> None:
        """Demonstrate basic vector search capabilities."""
        self._log_section("VECTOR SEARCH")
        
        query_vector = data_generator.generate_random_vector(self.vector_size)
        
        # Basic vector search
        self.logger.info("[bold]Performing a basic vector search...[/bold]")
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=settings.DEFAULT_SEARCH_LIMIT
        )
        
        # Format results in a cleaner way
        self.console.print("[green]Basic search results:[/green]")
        for i, result in enumerate(search_result):
            self.console.print(f"  [bold]{i+1}.[/bold] ID: {result.id}, Score: {result.score:.4f}")
            self.console.print(f"     Category: {result.payload['category']}, Rating: {result.payload['score']}")
        
        # Vector search with filtering
        self.logger.info("\n[bold]Performing vector search with payload filtering...[/bold]")
        filtered_search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(value="electronics")
                    ),
                    models.FieldCondition(
                        key="score",
                        range=models.Range(
                            gte=5.0,
                        )
                    )
                ]
            ),
            limit=settings.DEFAULT_SEARCH_LIMIT
        )
        
        self.console.print("[green]Filtered search results (electronics with score >= 5.0):[/green]")
        for i, result in enumerate(filtered_search_result):
            self.console.print(f"  [bold]{i+1}.[/bold] ID: {result.id}, Score: {result.score:.4f}")
            self.console.print(f"     Category: {result.payload['category']}, Rating: {result.payload['score']}")
    
    def demonstrate_scrolling(
        self, 
        batches: int = settings.DEFAULT_BATCH_COUNT, 
        batch_size: int = settings.DEFAULT_BATCH_SIZE
    ) -> None:
        """
        Demonstrate scrolling API for pagination.
        
        Args:
            batches: Number of batches to retrieve
            batch_size: Size of each batch
        """
        self._log_section("SCROLLING PAGINATION")
        
        self.logger.info(f"[bold]Demonstrating scrolling API with {batch_size} points per batch...[/bold]")
        offset = None
        
        for i in range(batches):
            self.console.print(f"[yellow]Fetching batch {i+1}...[/yellow]")
            
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
            points = scroll_result[0]
            offset = scroll_result[1]
            
            self.console.print(f"[green]Batch {i+1} summary:[/green]")
            self.console.print(f"  • Retrieved [bold]{len(points)}[/bold] points")
            self.console.print(f"  • Categories: " + 
                  ", ".join(set(p.payload['category'] for p in points)))
            self.console.print(f"  • Next offset: [bold]{offset}[/bold]")
            
            if offset is None:
                self.console.print("[italic]No more points to retrieve[/italic]")
                break
    
    def get_cluster_stats(self) -> None:
        """Get collection and cluster statistics."""
        self._log_section("COLLECTION STATISTICS")
        
        # Collection stats
        self.logger.info("Fetching collection information and statistics...")
        collection_info = self.client.get_collection(self.collection_name)
        
        # Display formatted stats
        self.console.print("[green]Collection Statistics:[/green]")
        self.console.print(f"  • Status: [bold]{collection_info.status}[/bold]")
        self.console.print(f"  • Vector count: [bold]{collection_info.vectors_count}[/bold]")
        self.console.print(f"  • Points count: [bold]{collection_info.points_count}[/bold]")
        self.console.print(f"  • Segments count: [bold]{collection_info.segments_count}[/bold]")
        self.console.print(f"  • Shard number: [bold]{collection_info.config.params.shard_number}[/bold]")
        self.console.print(f"  • Vector size: [bold]{collection_info.config.params.vectors.size}[/bold]")
        self.console.print(f"  • Distance metric: [bold]{collection_info.config.params.vectors.distance}[/bold]")
        
        self.logger.info("Note: Cluster information not available in this version of Qdrant")
    
    def run_demo(self) -> None:
        """Run the complete demonstration."""
        self.console.print("[bold green]STARTING QDRANT MULTI-NODE CLUSTER DEMO[/bold green]")
        self.console.print("[bold yellow]========================================[/bold yellow]")
        
        try:
            self.setup_collection()
            self.insert_data()
            self.demonstrate_vector_search()
            self.demonstrate_scrolling()
            self.get_cluster_stats()
            
            self.console.print("\n[bold green]Demo completed successfully![/bold green]")
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
            raise 