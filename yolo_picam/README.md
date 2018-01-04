#### Copy index.html for serving video
```
cp index.html /var/www/html/
```

#### Get YOLO model weights
```
wget https://www.dropbox.com/s/xastcd4c0dv2kty/tiny.h5?dl=0 -O tiny.h5
```

#### Run the script in the background
```
nohup sudo python3 picam.py &
```

