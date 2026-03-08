import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def fonlari_cek():
    # TEFAS'ın tüm fonları listelediği ana tablo sayfası
    url = "https://www.tefas.gov.tr/FonKarsilastirma.aspx"
    
    # TEFAS bizi bot sanıp engellemesin diye normal bir insan/tarayıcı gibi davranıyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print("TEFAS'a bağlanılıyor...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Sayfadaki tüm fonların olduğu tabloyu buluyoruz
        tablo = soup.find('table', id='MainContent_gwFunds')
        satirlar = tablo.find('tbody').find_all('tr')
        
        fon_verileri = {}
        
        # Tablodaki her bir satırı (yani her bir fonu) tek tek okuyoruz
        for satir in satirlar:
            sutunlar = satir.find_all('td')
            if len(sutunlar) > 2:
                fon_kodu = sutunlar[0].text.strip()
                
                # Fiyatı alıp, virgülü noktaya çeviriyoruz (yazılım diline uygun olsun diye)
                fiyat_metni = sutunlar[2].text.strip().replace(',', '.')
                
                try:
                    fiyat = float(fiyat_metni)
                    fon_verileri[fon_kodu] = fiyat
                except ValueError:
                    continue
        
        # Çektiğimiz verileri senin uygulamanın okuyacağı JSON formatında hazırlıyoruz
        sonuc = {
            "guncellenme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fonlar": fon_verileri
        }
        
        # fon_fiyatlari.json adlı dosyaya kaydediyoruz
        with open("fon_fiyatlari.json", "w", encoding="utf-8") as f:
            json.dump(sonuc, f, ensure_ascii=False, indent=4)
            
        print(f"Başarılı! Toplam {len(fon_verileri)} adet fon çekildi.")
        
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    fonlari_cek()
