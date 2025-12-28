 import qrcode
from PIL import Image

class UPIQRGenerator:
    def generate_upi_link(self, vpa, name, amount, note):
        if not vpa or "@" not in vpa:
            raise ValueError("Invalid VPA (UPI ID)")
            
        params = [f"pa={vpa}"]
        if name: params.append(f"pn={name}")
        if amount: params.append(f"am={amount}&cu=INR")
        if note: params.append(f"tn={note}")
        
        return "upi://pay?" + "&".join(params)

    def generate_qr(self, vpa, name, amount, note, logo_path=None, fg_color="black", bg_color="white"):
        upi_url = self.generate_upi_link(vpa, name, amount, note)
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        fg = fg_color if fg_color else "black"
        bg = bg_color if bg_color else "white"
        
        try:
            img = qr.make_image(fill_color=fg, back_color=bg).convert('RGB')
        except:
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        if logo_path:
            try:
                logo = Image.open(logo_path)
                basewidth = int(img.size[0] / 4)
                wpercent = (basewidth / float(logo.size[0]))
                hsize = int((float(logo.size[1]) * float(wpercent)))
                logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                
                pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                
                if 'A' in logo.getbands():
                    img.paste(logo, pos, mask=logo)
                else:
                    img.paste(logo, pos)
            except Exception:
                pass
                
        return img
