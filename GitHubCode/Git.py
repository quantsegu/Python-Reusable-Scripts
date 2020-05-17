from git import Repo
import sys
from git import Git

RepositoryPath = r'https://github.com/quantsegu/blockly'
DestinationPath = r'C:\Users\segul\OneDrive\Documents\Test3'

# Repo.clone_from(RepositoryPath, DestinationPath)
g =Git(DestinationPath)
g.checkout('v1.0')