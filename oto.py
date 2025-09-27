from playwright.sync_api import sync_playwright,Error
from playwright_stealth.stealth import Stealth
from time import sleep
import requests
from random import uniform
import os

def run_checker():
    """
    Bu ana fonksiyon, bir tarayıcı oturumu başlatır, giriş yapar ve
    başarılı olursa sonsuz bir döngü içinde veri kontrolü yapar.
    Tarayıcı çökerse veya kritik bir hata olursa, fonksiyon sona erer.
    """
    with sync_playwright() as p:
        browser=None
        try:
            browser=p.firefox.launch(
                headless=True,
                slow_mo=300
        )
            context=browser.new_context()
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
            page=context.new_page()
            username = os.environ.get("BIONLUK_USERNAME")
            password = os.environ.get("BIONLUK_PASSWORD")
            if not username or not password:
                print("HATA: BIONLUK_USERNAME ve BIONLUK_PASSWORD gizli değişkenleri ayarlanmamış.")
                return
            page.goto("https://bionluk.com/login")
            sleep(uniform(2,4))
            page.get_by_placeholder("E-posta veya kullanıcı adı").fill(username)
            sleep(uniform(1,2))
            page.get_by_placeholder("Şifre").fill(password)
            sleep(uniform(1,2))
            page.get_by_role("button",name="Giriş Yap").click()
            sleep(uniform(60,90))
            page.goto("https://bionluk.com/panel/alici-istekleri")
            sleep(uniform(2,4))
            name=page.locator("#app div.bodyContainer > div.pageContainer div.content div.request-box").first
            name.wait_for(state='visible', timeout=25000)
            name1=name.locator("div.body p.body-title").inner_text()
            print(f"Takip başlıyor. Mevcut ilk başlık: {name1}")
            while True:
                wait_time = uniform(360, 600)
                print(f"{int(wait_time / 60)} dakika sonra sayfa yenilenecek...")
                sleep(wait_time)
                try:
                    page.reload(wait_until='domcontentloaded')
                    name.wait_for(state='visible', timeout=25000)
                    name2 = name.locator("div.body p.body-title").inner_text()

                    if name2 != name1:
                        bildirim(name2)
                        name1 = name2
                except Error as e:
                    print(f"İç döngüde bir Playwright hatası oluştu (örn: sayfa yüklenemedi): {e}")
                    print("Kurtarma deneniyor: Sayfaya yeniden gidiliyor...")
                    # Hata durumunda kurtarma için sayfaya yeniden gitmeyi dene
                    page.goto("https://bionluk.com/panel/alici-istekleri")
        
        
        finally:
            browser.close()

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


run_checker()


