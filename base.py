import base64

# Read the image file
image_data = open('newbadges/SilverII.png', 'rb').read()

# Encode as base64
data_uri = base64.b64encode(image_data).decode('utf-8')

# Create an <img> tag with the base64-encoded image
img_tag = f'<img src="data:plot/png;base64,{data_uri}" alt="Generated Image">'
print(img_tag)