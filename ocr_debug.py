from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import pytesseract

# Update path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 👇 Set your receipt image here
image_path = "your_receipt.jpg"

# Preprocess image
image = Image.open(image_path)
image = image.convert("L")
image = image.resize((image.width * 2, image.height * 2))
image = image.filter(ImageFilter.SHARPEN)
image = ImageEnhance.Contrast(image).enhance(3.0)
image = image.convert("RGB")  # required for drawing

# Run OCR with bounding box data
data = pytesseract.image_to_data(image, config="--psm 6", output_type=pytesseract.Output.DICT)
draw = ImageDraw.Draw(image)

# Draw boxes around each detected word
for i in range(len(data["text"])):
    word = data["text"][i]
    conf = int(data["conf"][i])
    if word.strip() and conf > 60:
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
        draw.text((x, y - 12), word, fill="blue")

# Show the image with boxes
image.show()
