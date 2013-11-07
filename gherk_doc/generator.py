from datetime import datetime

import os
import re
import unicodedata
import shutil

from jinja2 import FileSystemLoader, Environment, Undefined
from behave.parser import ParserError, DEFAULT_LANGUAGE, Parser

class Generator(object):

    DEFAULT_TEMPLATE_DIRECTORY = 'templates'

    INDEX_TEMPLATE = 'index.html'

    features = []

    project_name = None

    templates_directory = None

    def __init__(self, project_name, templates_directory=DEFAULT_TEMPLATE_DIRECTORY):
        self.project_name = project_name
        self.templates_directory = templates_directory

        self.environment = Environment(loader=FileSystemLoader(templates_directory), trim_blocks=True)
        self.environment.filters['slugify'] = self.slugify

    def add_feature(self, path):
        with open(path, 'rb') as feature_file:
            # file encoding is assumed to be utf8. Oh, yes.
            data = feature_file.read().decode('utf8').strip()

            # ALL data operated on by the parser MUST be unicode
            assert isinstance(data, unicode)

            try:
                if data:
                    feature = Parser(DEFAULT_LANGUAGE).parse(data, path)
                else:
                    raise ParserError("Empty file", line=0)

                if feature is None:
                    raise ParserError("Unknown reasons", line=0)
                else:
                    self.features.append(feature)
            except ParserError, e:
                e.filename = path
                raise

    def render(self):
        return self.environment.get_template(Generator.INDEX_TEMPLATE).render(
            project_name=self.project_name,
            features=self.features,
            generation_time=datetime.now().isoformat()
        )

    def generate(self, output):
        output = os.path.abspath(output)

        if os.path.exists(output):
            shutil.rmtree(output)

        shutil.copytree(self.templates_directory, output, False, shutil.ignore_patterns(Generator.INDEX_TEMPLATE))

        with open(os.path.join(output, Generator.INDEX_TEMPLATE), 'w') as index_output:
            index_output.write(self.render().encode("utf-8"))

    @staticmethod
    def slugify(title):
        """
        Converts to lowercase, removes non-word characters (alphanumerics and
        underscores) and converts spaces to hyphens. Also strips leading and
        trailing whitespace.
        """
        if isinstance(title, Undefined):
            return None

        title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii')
        title = re.sub('[^\w\s-]', '', title).strip().lower()

        return re.sub('[-\s]+', '-', title)