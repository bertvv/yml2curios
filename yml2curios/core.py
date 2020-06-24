# -*- coding: utf-8 -*-

import os
import random
from glob import glob
from zipfile import ZipFile

import jinja2

TEMPLATE_DIR = "%s/templates/" % os.getcwd()
TEMPLATE_LOADER = jinja2.FileSystemLoader(searchpath = TEMPLATE_DIR)
TEMPLATE_ENVIRONMENT = jinja2.Environment(loader = TEMPLATE_LOADER)


def process_questions(title, questions, output_dir):
    """Iterate over the questions and convert them to XML."""
    question_index = 1
    for question in questions:
        validate(question)
        question['title'] = "%s %05d" % (title, question_index)
        outf = open("%s/%s_%05d.xml" % (output_dir, title, question_index), "w")
        outf.write(to_xml(question))
        outf.close()
        question_index = question_index + 1


def validate(question):
    """Predicate that checks whether the specified question is in the
       correct format"""
    # There should be a file with name templates/TYPE.xml.j2
    template_path = TEMPLATE_DIR + question["type"] + ".xml.j2"
    if(not os.path.exists(template_path)):
        raise FileNotFoundError(
            "There is no template available for question type %s" %
            question["type"])
    return True


def to_xml(question):
    """Converts the specified question to the Curios XML format, using a Jinja
       template suitable for the question type."""
    template = TEMPLATE_ENVIRONMENT.get_template(
        question["type"] + ".xml.j2")

    return template.render(question)


def package_questions(title, output_dir):
    """Create a zip file containing all questions from the series with the
       specified title."""
    # Go to the output directory
    os.chdir(output_dir)

    # First, select all the files
    question_files_xml = glob("%s_*.xml" % title)
    question_files = [xml.replace('xml', 'zip') for xml in question_files_xml]

    # Convert them to .zip
    for idx in range(len(question_files_xml)):
        print("Zipping %s -> %s" %
            (question_files_xml[idx], question_files[idx]))
        with ZipFile(question_files[idx], 'w') as zipfile:
            zipfile.write(question_files_xml[idx])
            zipfile.close()
    
    # Then, create the index.xml file
    index_template = TEMPLATE_ENVIRONMENT.get_template("index.xml.j2")
    index_file = open("index.xml", "w")
    index_file.write(index_template.render({
        "question_files": question_files,
        "id": "%05d" % random.randint(1,99999),
        "title": title
    }))
    index_file.close()

    # Finally, create a new zip containing all the other zips and the index
    with ZipFile("%s.zip" % title, "w") as zipfile:
        zipfile.write("index.xml")
        for qfile in question_files:
            zipfile.write(qfile)
        zipfile.close()