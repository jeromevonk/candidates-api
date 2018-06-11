import zipfile
import os

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

zf = zipfile.ZipFile('candidates_api.zip', mode='w', compression=zipfile.ZIP_DEFLATED)

zf.write('candidates_api.py')
zf.write('requirements.txt')
zf.write('Pipfile')
zf.write('Pipfile.lock')

# Folder 'ebextensions'
zipdir('.ebextensions/', zf)

# Folder 'static'
zipdir('static/', zf)

# Folder 'templates'
zipdir('templates/', zf)

zf.close()

