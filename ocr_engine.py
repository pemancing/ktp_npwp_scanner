from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ind')

def extract_text(image_path):
    result = ocr.ocr(image_path, cls=True)
    lines = []
    for line in result[0]:
        lines.append(line[1][0])
    return "\n".join(lines)
