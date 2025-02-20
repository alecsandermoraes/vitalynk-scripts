from pyzbar import pyzbar 
from PIL import Image 
import cv2, re 
import qrcode

class QRCode:
    
    def __init__(self, size = 10, border = 4, fill_color = 'black', back_color = 'white'):
        self.size = size 
        self.border = border 
        self.fill_color = fill_color 
        self.back_color = back_color 
        
    def Generate(self, data: str, output_path: str, logo_path: str = None):
        qr = qrcode.QRCode(
            version = None, 
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = self.size, 
            border = self.border
        )
        
        qr.add_data(data)
        qr.make(fit = True)
        
        qr_img = qr.make_image(fill_color = self.fill_color, back_color = self.back_color).convert('RGBA')

        if logo_path:
            try:
                logo = Image.open(logo_path)
                qr_width, qr_height = qr_img.size 
                logo_size = qr_width // 4 
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                qr_img.paste(logo, pos, mask = logo if logo.mode == 'RGBA' else None)
            except Exception as e:
                print(f'[vitalynk.qrcode] Erro ao Adicionar Logotipo: {e}')
        
        qr_img.save(output_path)
        
    def Read(self, image_path: str) -> str:
        img = cv2.imread(image_path)
        detected_qrs = pyzbar.decode(img)
        if detected_qrs:
            return detected_qrs[0].data.decode('utf-8')
        else:
            raise ValueError('[vitalynk.qrcode] Nenhum QR Code detectado na imagem')

    def Validate(self, qr_data: str) -> bool:
        url_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#]*$')
        return bool(url_pattern.match(qr_data))

    def ExtractMetadata(self, image_path: str) -> dict:
        img = cv2.imread(image_path)
        detected_qrs = pyzbar.decode(img)
        if not detected_qrs:
            raise ValueError('[vitalynk.qrcode] Nenhum QR Code detectado na imagem')
        qr_info = detected_qrs[0]
        
        metadata = {
            'data': qr_info.data.decode('utf-8'),
            'type': qr_info.type,
            'rect': {
                'x': qr_info.rect.left,
                'y': qr_info.rect.top,
                'width': qr_info.rect.width,
                'height': qr_info.rect.height,
            }
        }
        
        return metadata 
    