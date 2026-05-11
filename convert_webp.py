from PIL import Image
import os

cities_dir = r'C:\Users\Admin\cleaning-site\img\cities'
files = ['dnipro.jpg', 'lviv.jpg', 'kharkiv.jpg', 'odessa.jpg']

for filename in files:
    src = os.path.join(cities_dir, filename)
    dst = os.path.join(cities_dir, filename.replace('.jpg', '.webp'))
    img = Image.open(src)
    img.save(dst, 'WEBP', quality=82)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    print(f'{filename} -> {filename.replace(".jpg", ".webp")}  ({src_size//1024}KB -> {dst_size//1024}KB)')

print('Done.')
