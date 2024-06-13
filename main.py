from lib.loads import *

app_name = "Samsan Tech"

source_type = 'video'

image_path = 'source/gambar2.jpg'
video_path = 'source/video1.mp4'
url_path = "http://192.168.1.248:8080/video"

# Contoh Pemakaian:
# main('Samsan Tech', 'image', 'path/to/image.jpg')
# main('Samsan Tech', 'video', 'path/to/video.mp4', scale_percent=50)
# main('Samsan Tech', 'url', 'http://your-video-url', scale_percent=50)

if __name__ == "__main__":
    # Image File
    # main(app_name, source_type, image_path)
    
    # Video File
    main(app_name, source_type, video_path, scale_percent=50)
    
    # Video Url
    # main(app_name, source_type, url_path, scale_percent=50)