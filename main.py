from tefas import Crawler
import json
from datetime import datetime, timedelta

def fonlari_cek():
    crawler = Crawler()
    bugun = datetime.now()
    
    print("TEFAS verileri tefas-crawler ile çekiliyor...")
    
    try:
        # Hafta sonu veya tatil olma ihtimaline karşı son 4 günün verisini isteyelim
        baslangic = (bugun - timedelta(days=4)).strftime("%Y-%m-%d")
        bitis = bugun.strftime("%Y-%m-%d")
        
        data = crawler.fetch(start=baslangic, end=bitis)
        
        if data is not None and not data.empty:
            # En güncel tarihi bul
            en_guncel_tarih = data['date'].max()
            guncel_data = data[data['date'] == en_guncel_tarih]
            
            fon_verileri = {}
            for index, row in guncel_data.iterrows():
                fon_verileri[row['code']] = float(row['price'])
                
            sonuc = {
                "guncellenme_zamani": bugun.strftime("%Y-%m-%d %H:%M:%S"),
                "tefas_verisi_tarihi": str(en_guncel_tarih),
                "fonlar": fon_verileri
            }
            
            with open("fon_fiyatlari.json", "w", encoding="utf-8") as f:
                json.dump(sonuc, f, ensure_ascii=False, indent=4)
                
            print(f"Başarılı! Toplam {len(fon_verileri)} adet fon {en_guncel_tarih} tarihiyle çekildi.")
        else:
            print("Belirtilen tarihler arasında veri bulunamadı!")
            
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    fonlari_cek()
