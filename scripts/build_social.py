"""Build the simple typography-only Open Graph card using Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
image = Image.new('RGB',(1200,630),'#0f172a')
draw = ImageDraw.Draw(image)
def font(size):
    for path in ['C:/Windows/Fonts/arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if Path(path).exists(): return ImageFont.truetype(path,size)
    return ImageFont.load_default(size=size)
draw.ellipse((850,-200,1400,350),outline='#243552',width=2)
draw.text((85,90),'ADMINISTRATIVE PORTFOLIO',font=font(23),fill='#93b7ff')
draw.text((85,185),'Thoughtful support.\nOrganized work.',font=font(65),fill='white',spacing=15)
draw.text((85,410),'Aspiring Virtual Administrative Assistant',font=font(30),fill='#cbd5e1')
draw.rounded_rectangle((85,505,430,558),radius=8,fill='#2563eb')
draw.text((110,518),'Explore my practice projects',font=font(21),fill='white')
image.save(root/'static/images/social-card.png',optimize=True)
