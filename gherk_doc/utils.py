import os
import fnmatch

def find_features(path, absolute=True):
    feature_files = []

    for root, dirnames, filenames in os.walk(path):
      for filename in fnmatch.filter(filenames, '*.feature'):

          feature_file_path = os.path.join(root, filename)

          if absolute:
              feature_file_path = os.path.abspath(feature_file_path)

          feature_files.append(feature_file_path)

    return feature_files