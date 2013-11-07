from os import path

from .generator import Generator
from .utils import find_features

bundled_template_path = path.join(path.abspath(path.dirname(__file__)), 'templates')
