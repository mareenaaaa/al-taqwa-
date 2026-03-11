from PIL import Image

def process_logo_v2():
    try:
        img = Image.open('logo2.jpeg').convert('RGBA')
        img_data = img.load()
        W, H = img.size
        
        # Determine background color by sampling the top-left corner
        bg_color = img_data[0, 0]
        
        # Let's just create a version where all pixels close to bg_color are transparent
        # And let's crop empty space
        min_x, min_y = W, H
        max_x, max_y = 0, 0
        
        for y in range(H):
            for x in range(W):
                r, g, b, a = img_data[x, y]
                # Distance from bg_color
                dist = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
                if dist > 30: # It's foreground
                    if x < min_x: min_x = x
                    if x > max_x: max_x = x
                    if y < min_y: min_y = y
                    if y > max_y: max_y = y
        
        if min_x > max_x:
            print("Could not find logo boundaries")
            # fallback
            img.save('logo2_cropped.png')
            return
            
        # Add padding
        padding = 10
        crop_box = (max(0, min_x - padding), max(0, min_y - padding), 
                    min(W, max_x + padding), min(H, max_y + padding))
                    
        cropped = img.crop(crop_box)
        c_data = cropped.load()
        cW, cH = cropped.size
        
        for y in range(cH):
            for x in range(cW):
                r, g, b, a = c_data[x, y]
                # Assuming background was white, and text was black/colored
                # To be safe, if we want it white on transparent:
                dist = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
                if dist < 40:
                    c_data[x, y] = (255, 255, 255, 0) # Transparent bg
                else: # It's text
                    # Make it pure white
                    c_data[x, y] = (255, 255, 255, min(dist * 2, 255))
                    
        cropped.save('logo2_cropped.png')
        print('Successfully processed logo2')
    except Exception as e:
        print("Error:", e)

process_logo_v2()
