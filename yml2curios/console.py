# -*- coding: utf-8 -*-

import os
import re

import click
import yaml

from . import __version__
from yml2curios.core import process_questions, package_questions

@click.command()
@click.version_option(version=__version__)
@click.option('-o', '--output-dir', default = "out", show_default=True)
@click.argument("questionfile", type=click.File('rb'))
def main(output_dir, questionfile):
    """Create a series of questions for the Curios assessment platform from the
       specified YAML file."""
    click.echo("Reading from %s" % questionfile.name)

    # Extract the file name (without extension) from the path
    title = re.sub(r'.*/([^/]*).yml', r'\1', questionfile.name)

    # Parse the YAML file containing the questions
    questions = yaml.full_load(questionfile)

    # Ensure the output directory exists
    if (not os.path.isdir(output_dir)):
        click.echo("Creating output directory %s" % output_dir)
        os.mkdir(output_dir)

    # Convert each question
    process_questions(title, questions, output_dir)
    
    # Create zip archive containing these questions
    package_questions(title, output_dir)
