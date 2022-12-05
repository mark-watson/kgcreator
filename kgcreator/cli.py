import click
from .kgcreator import *

@click.command()
@click.version_option()
@click.option("--inputdir", help="File path to directory containing text files")
@click.option("--outputfile", help="File name for generated RDF")
@click.option("--outputfileneo4j", help="File name for generated Neo4J Cypher data")
def cli(inputdir, outputfile, outputfileneo4j):
    "Knowledge Graph Creator: converts text to RDF triples.\n\ne.g., kgcreator --inputdir=test_data --outputfile=out.rdf"
    process_directory(inputdir, outputfile, outputfileneo4j)

