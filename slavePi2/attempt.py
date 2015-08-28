import os

print os.stat("image.data")
with open ("image.data", "rb") as f:
	print repr(f.read())
