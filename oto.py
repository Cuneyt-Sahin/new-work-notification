import os
import requests
from time import sleep
from random import uniform
from playwright.sync_api import sync_playwright, Error as PlaywrightError
from playwright_stealth.stealth import Stealth

def bildirim(mesaj):
    if mesaj is None:
        print("Bildirime gönderilecek mesaj boş (None), gönderme işlemi atlandı.")
        return 
    konu="istakipsistemixycz"
    try:
        requests.post(
            f"https://ntfy.sh/{konu}",
            data=mesaj.encode('utf-8'), # Türkçe karakterler için
            headers={
                "Title": "Yeni is ilani", # Bildirimin başlığı
                "Priority": "high", # Yüksek öncelik
                "Tags": "tada" # Bildirim ikonu (tada, warning, etc.)
            }
        )
    except Exception as e:
        print(e)


def fetch_latest_request_title():
    """
    Tek bir görev yapar: Tarayıcıyı açar, giriş yapar, ilk başlığı alır ve tarayıcıyı kapatır.
    Başarılı olursa başlığı, başarısız olursa None döndürür. Bu bizim "İşçi"miz.
    """
    print("\n--- Yeni Kontrol Başlatılıyor ---")
    with sync_playwright() as p:
        browser = None
        try:
            browser = p.firefox.launch(headless=True, slow_mo=300)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            )
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            context.add_init_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        // This array simulates common browser plugins.
                        // You can adjust its length or content if specific sites require more realism.
                        { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
                        { name: 'Chrsome PDF Viewer', filename: 'mhjfbmdgcfjbbgcljjhdiojgimefjhie', description: '' },
                        { name: 'Native Client', filename: 'internal-nacl-plugin', description: '' }
                    ]
                });
            """)
            context.add_init_script("""
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """)
            Stealth().apply_stealth_sync(context)
            page = context.new_page()
            
            print("Giriş sayfasına gidiliyor...")
            page.goto("https://bionluk.com/login")
            
            username = "cuneytsahin.17.17@gmail.com"#os.environ.get('BIONLUK_USERNAME')
            password = "sahinkaplaN.12"#os.environ.get('BIONLUK_PASSWORD')

            if not username or not password:
                print("HATA: BIONLUK_USERNAME ve BIONLUK_PASSWORD gizli değişkenleri ayarlanmamış.")
                return None

            page.get_by_placeholder("E-posta veya kullanıcı adı").fill(username)
            page.get_by_placeholder("Şifre").fill(password)
            page.get_by_role("button", name="Giriş Yap").click()
            sleep(uniform(60,90))
            # BURASI ÇOK ÖNEMLİ: EĞER MAİL ONAYI GEREKİYORSA, BU OTOMASYON ÇALIŞMAZ.
            # BU KISMI MANUEL OLARAK ONAYLADIĞINI VARSAYIYORUZ.
            print("Giriş yapılıyor, panelin yüklenmesi bekleniyor...")
            print("Giriş başarılı!")
            
            print("Alıcı istekleri sayfasına gidiliyor...")
            page.goto("https://bionluk.com/panel/alici-istekleri")
            
            request_box_locator = page.locator("#app div.bodyContainer > div.pageContainer div.content div.request-box").first
            request_box_locator.wait_for(state='visible', timeout=25000)
            
            title = request_box_locator.locator("div.body p.body-title").inner_text()
            print(f"Başlık başarıyla alındı: {title}")
            
            return title
            
        except Exception as e:
            print(f"İşlem sırasında bir hata oluştu: {e}")
            if 'page' in locals():
                page.screenshot(path="hata.png")
            return None
        
        finally:
            if browser:
                browser.close()
                print("Tarayıcı kapatıldı.")

# --- ANA PROGRAM (YÖNETİCİ) ---
if __name__ == "__main__":
    last_known_title = None
    
    # Program ilk çalıştığında bir kerelik başlığı alıp hafızaya kaydet
    print("Program başlıyor, ilk başlık alınıyor...")
    last_known_title = fetch_latest_request_title()
    if last_known_title:
        print(f"Takip başlıyor. Mevcut ilk başlık: {last_known_title}")
    else:
        print("İlk başlık alınamadı, 10 dakika sonra tekrar denenecek.")

    while True:
        wait_time = uniform(360, 600)
        print(f"\n{int(wait_time / 60)} dakika bekleniyor...")
        sleep(wait_time)
        
        # Yeni başlığı almak için "işçi" fonksiyonunu tekrar çağır
        new_title = fetch_latest_request_title()
        
        if new_title is not None and new_title != last_known_title:
            print("!!!!!!!!!!!!!!!!!!!!!! YENİ İŞ İSTEĞİ BULUNDU !!!!!!!!!!!!!!!!!!!")
            bildirim(new_title)
            last_known_title = new_title
        elif new_title is None:
            print("Bu turda başlık alınamadı, döngü devam ediyor.")
        else:
            print("Yeni bir istek bulunamadı, başlık aynı.")