import os
import base64

# Images path
path = '.'  

# Get a list of imagems inside the directory
images = os.listdir(path)

# For each image, detect the face and add to the list
print('Checking path: {}'.format(path) )
for image in images:
    
    # Skip files that are not images
    if ".jpg" not in image:
        continue
        
    # Print file name
    print(image)
    
    # Read and encode
    with open(path + "/" + image, 'rb') as fi:
        content = fi.read()
        encoded = base64.b64encode(content)
        
    # Write
    with open(path + "/" + image + '.b64', 'wb') as fo:
        fo.write(encoded)
