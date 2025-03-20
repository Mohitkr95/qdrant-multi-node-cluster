#!/usr/bin/env python3
"""
Main entry point to run the Qdrant cluster demonstration.
"""

import argparse
import logging

from qdrant_demo.core.cluster_demo import QdrantClusterDemo
from qdrant_demo.config import settings


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Qdrant cluster demonstration")
    
    parser.add_argument(
        "--host", 
        type=str, 
        default=settings.QDRANT_HOST,
        help=f"Qdrant host (default: {settings.QDRANT_HOST})"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=settings.QDRANT_PORT,
        help=f"Qdrant port (default: {settings.QDRANT_PORT})"
    )
    
    parser.add_argument(
        "--points", 
        type=int, 
        default=settings.DEFAULT_POINT_COUNT,
        help=f"Number of points to insert (default: {settings.DEFAULT_POINT_COUNT})"
    )
    
    return parser.parse_args()


def main():
    """Run the Qdrant cluster demo."""
    args = parse_args()
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting Qdrant demo with host={args.host}, port={args.port}")
    
    try:
        # Create and run the demo
        demo = QdrantClusterDemo(host=args.host, port=args.port)
        demo.run_demo()
        
    except Exception as e:
        logger.error(f"Error running demo: {e}")
        raise


if __name__ == "__main__":
    main() 