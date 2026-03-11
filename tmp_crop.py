from PIL import Image

def process_logo():
    img = Image.open('logo2.jpeg').convert('RGBA')
    W, H = img.size
    pixels = img.load()
    
    # 1. We know the logo is black on a white circle, in the center of a dark screen.
    # Let's find the bounding box of the black pixels that are within the center region.
    min_x, min_y = W, H
    max_x, max_y = 0, 0
    
    for y in range(H):
        for x in range(W):
            r, g, b, a = pixels[x, y]
            # Dark pixel
            if r < 100 and g < 100 and b < 100:
                # To distinguish logo from dark background, check if there's white nearby or if it's near center
                # Specifically, the logo is surrounded by white. But a simpler way is:
                # The phone background is dark, the circle is white.
                pass

    # A better approach: 
    # Just turn the white circle into transparent, and extract only the black logo, and crop exactly.
    # Or, even simpler: since the user said "cut the logo correctly", they might just want the white circle cropped!
    # Because a logo inside a white circle looks good on a dark header if cropped correctly!
    
    # Let's find the bounding box of the *white circle*.
    wc_min_x, wc_min_y = W, H
    wc_max_x, wc_max_y = 0, 0
    for y in range(H):
        for x in range(W):
            r, g, b, a = pixels[x, y]
            if r > 240 and g > 240 and b > 240: # White pixel
                # Ignore top status bar (y < H * 0.1)
                if y > H * 0.1 and y < H * 0.9:
                    if x < wc_min_x: wc_min_x = x
                    if x > wc_max_x: wc_max_x = x
                    if y < wc_min_y: wc_min_y = y
                    if y > wc_max_y: wc_max_y = y
                    
    print("White circle bounds:", wc_min_x, wc_min_y, wc_max_x, wc_max_y)
    
    # Now find the bounding box of the *black logo* inside the white circle
    bl_min_x, bl_min_y = W, H
    bl_max_x, bl_max_y = 0, 0
    
    for y in range(wc_min_y, wc_max_y+1):
        for x in range(wc_min_x, wc_max_x+1):
            r, g, b, a = pixels[x, y]
            if r < 100 and g < 100 and b < 100: # Black pixel
                if x < bl_min_x: bl_min_x = x
                if x > bl_max_x: bl_max_x = x
                if y < bl_min_y: bl_min_y = y
                if y > bl_max_y: bl_max_y = y
                
    print("Black logo bounds:", bl_min_x, bl_min_y, bl_max_x, bl_max_y)

    # We will make an image that contains just the black logo, but painted white, on a transparent background!
    # Let's add some padding
    padding = 20
    crop_box = (max(0, bl_min_x - padding), max(0, bl_min_y - padding), 
                min(W, bl_max_x + padding), min(H, bl_max_y + padding))
                
    cropped = img.crop(crop_box)
    
    # Now, make all white pixels transparent, and all black pixels white!
    c_pixels = cropped.load()
    cW, cH = cropped.size
    for y in range(cH):
        for x in range(cW):
            r, g, b, a = c_pixels[x, y]
            # Convert to grayscale to evaluate
            gray = (r + g + b) // 3
            if gray > 150:
                # White-ish background -> transparent
                c_pixels[x, y] = (255, 255, 255, 0)
            else:
                # Black-ish text -> white text, alpha depends on darkness for anti-aliasing
                alpha = 255 - gray
                c_pixels[x, y] = (255, 255, 255, alpha)

    cropped.save('logo2_cropped.png')
    print('Completed cropping and transparency!')

process_logo()
