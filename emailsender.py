from bs4 import BeautifulSoup
# make sure to have bs installed
import requests
import shutil
import glob
import time
import os



URL = "https://www.reddit.com/r/dankmemes/"
# my pc user agent
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

# get the html
page = requests.get(URL, headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')

biggest_i = 0

# Creates a Memes directory, if the directory exists it just prints a message
try:
	os.mkdir('Memes')
	print('Done')
except FileExistsError:
	print('Already exists')


# Creates a list of elements in the Meme directory
memes_collected = os.listdir('Memes')
# print(memes_collected)

# By default every directory has an element 'Thumbs.db', if there are no images(only thumbs.db)---> len == 1
# if we don't have any images, the index for the next meme should be 0
if len(memes_collected) == 1:
	index = 0
else:
	# If we have some images, firstly we ignore the thumbs.db
	for i in memes_collected:
		if i == 'Thumbs.db':
			pass
		else:
			# Here we loop into all images until we find the biggest current index
			# This index + 1 is going to be used for the next set of images, so they don't get replaced by the same name
			# (We want to keep the names unique)
			index = int(i.split('#')[1].split('.')[0]) # <-- this just gets the value after (#) or the index
			if index > biggest_i:
				biggest_i = index

index = biggest_i
print('Biggest index: ', index)


# This block of code uses the source of the image and downloads it with a name and index from the above code
# Sets a unique name
def download_images(source, index):
	resp = requests.get(source, stream=True)
	local_file = open('Memes/meme#{0}.jpg'.format(index), 'wb')
	resp.raw.decode_content = True
	shutil.copyfileobj(resp.raw, local_file)
	del resp

# Checks into the reddit html for every <img> tag
for i in soup.find_all('img'):
	try:	
		# If the image is a post from a user i.e a meme, use the above code to download it with a unique name
		if i['alt'] == 'Post image':
			index += 1
			print(i['src'], index, '\n')
			download_images(i['src'], index)
	except:
		pass

	# print(i.img)
