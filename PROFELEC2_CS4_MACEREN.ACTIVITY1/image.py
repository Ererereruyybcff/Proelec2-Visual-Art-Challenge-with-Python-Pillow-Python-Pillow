from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# to create graident background
def create_gradient_background(width, height):
   
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
     
    for y in range(height): 
        ratio = y / height
        r = 255  # Keep red max for pink shades
        g = int(182 - ratio * 162)  # 182 → 20
        b = int(193 - ratio * 46)   # 193 → 147
        draw.rectangle([0, y, width, y+1], fill=(r, g, b))  
    return img

def add_glow_effect(img, text, position, font, base_color, glow_color, glow_radius=4):
    
    width, height = img.size
    glow_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    
    for r in range(glow_radius, 0, -1):
        alpha = int(100 * (glow_radius - r + 1) / glow_radius)
        glow_with_alpha = (*glow_color, alpha)
        
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if dx != 0 or dy != 0:
                    glow_draw.text((position[0] + dx, position[1] + dy),
                                   text, fill=glow_with_alpha, font=font)
    
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(radius=1.5))
    img = Image.alpha_composite(img.convert('RGBA'), glow_overlay)
    
    # Draw main text
    draw = ImageDraw.Draw(img)
    draw.text(position, text, fill=base_color, font=font)
    
    return img.convert('RGB')

def poster():
    # Create canvas with gradient background
    width, height = 800, 600
    poster = create_gradient_background(width, height)
    
    draw = ImageDraw.Draw(poster)
    
    # Font loader with fallbacks
    def load_font(size):
        font_paths = [
            "arial.ttf", "Arial.ttf", "ARIAL.TTF",  
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
        return ImageFont.load_default()
    
    # Load fonts
    title_font = load_font(65)
    slogan_font = load_font(35)
    subtitle_font = load_font(28)
    body_font = load_font(30)
    
    # Colors
    white = (255, 255, 255)
    purple = (138, 43, 226)
    cyan = (0, 255, 255)
    light_purple = (186, 85, 211)
    gold = (255, 215, 0)
    
    # Border in the poster
    border_thickness = 8
    draw.rectangle([border_thickness//2, border_thickness//2, 
                   width-border_thickness//2, height-border_thickness//2], 
                  outline=purple, width=border_thickness)
    
    college_text = "COLLEGE OF COMPUTING & INFORMATION SCIENCES"
    college_bbox = draw.textbbox((0, 0), college_text, font=subtitle_font)
    college_width = college_bbox[2] - college_bbox[0]
    draw.text(((width - college_width) // 2, 25), college_text, fill=cyan, font=subtitle_font)
    
    title_text = "CCIS PHANTOMS"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_pos = ((width - title_width) // 2, 70)
    poster = add_glow_effect(poster, title_text, title_pos, title_font, white, purple, 6)
    
    slogan_text = "Unleash the Phantoms!"
    slogan_bbox = draw.textbbox((0, 0), slogan_text, font=slogan_font)
    slogan_width = slogan_bbox[2] - slogan_bbox[0]
    slogan_pos = ((width - slogan_width) // 2, 150)
    poster = add_glow_effect(poster, slogan_text, slogan_pos, slogan_font, gold, (255, 140, 0), 4)
  
    draw = ImageDraw.Draw(poster)
  
    try:
        Ccislogo = Image.open("ccis.png").convert("RGBA")
        Ccislogo = Ccislogo.resize((300, 280), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(Ccislogo)
        Ccislogo = enhancer.enhance(1.2)

        mascot_x = (width - 300) // 2
        mascot_y = 210
        shadow = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse([5, 5, 295, 295], fill=(0, 0, 0, 50))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
        
        poster.paste(shadow, (mascot_x-5, mascot_y-5), shadow)
        poster.paste(Ccislogo, (mascot_x, mascot_y), Ccislogo)
    except FileNotFoundError:
        print("Mascot not found, drawing placeholder...")
        phantom_x, phantom_y = width // 2, 320
        phantom_size = 120
       
       
    bottom_y = height - 90
    draw.rectangle([30, bottom_y - 20, width - 30, height - 20], 
                  fill=(20, 20, 40), outline=purple, width=3)
    motto_parts = ["UNITED", "STRONG", "UNSTOPPABLE"]
    total_width = sum(draw.textbbox((0, 0), part, font=body_font)[2] - 
                     draw.textbbox((0, 0), part, font=body_font)[0] for part in motto_parts)
    separator_width = draw.textbbox((0, 0), " • ", font=body_font)[2] - draw.textbbox((0, 0), " • ", font=body_font)[0]
    total_text_width = total_width + 2 * separator_width
    start_x = (width - total_text_width) // 2
    current_x = start_x
    
    colors = [white, gold, cyan]
    for i, part in enumerate(motto_parts):
        draw.text((current_x, bottom_y + 10), part, fill=colors[i], font=body_font)
        part_width = draw.textbbox((0, 0), part, font=body_font)[2] - draw.textbbox((0, 0), part, font=body_font)[0]
        current_x += part_width
        if i < len(motto_parts) - 1:
            draw.text((current_x, bottom_y + 10), " • ", fill=light_purple, font=body_font)
            current_x += separator_width
    return poster

if __name__ == "__main__":
    print("Creating CCIS Phantoms poster (no particles)...")
    try:
        poster_img = poster()
        poster_img.save("ccis_phantoms_clean.png", 'PNG', quality=95)
        print("Poster saved as 'ccis_phantoms_clean.png'!")
        poster_img.show()
    except Exception as e:
        print(f"Error: {e}")
