import zipfile
import os

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

zf = zipfile.ZipFile('../bundle_aws.zip', mode='w', compression=zipfile.ZIP_DEFLATED)

zf.write('../candidates_api.py', 'candidates_api.py')
zf.write('../auxiliar.py', 'auxiliar.py')
zf.write('../models.py', 'models.py')
zf.write('../requirements.txt', 'requirements.txt')
zf.write('../Pipfile', 'Pipfile')
zf.write('../Pipfile.lock', 'Pipfile.lock')

# Folder 'ebextensions'
zipdir('../.ebextensions/', zf)

# Folder 'static'
zipdir('../static/', zf)

# Folder 'templates'
zipdir('../templates/', zf)

zf.close()

