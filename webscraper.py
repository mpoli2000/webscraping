import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

link = "https://index.hu"

def filter_proxies():
    """Obtiene una lista de proxies desde una fuente pública."""
    try:
        warnings.filterwarnings("ignore", category=UserWarning)
        response = requests.get('https://www.sslproxies.org/')
        # response = requests.get('https://free-proxy-list.net/', verify=False)
        # response = requests.get('https://proxyscrape.com/', verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        proxies = []
        for item in soup.select("table.table tbody tr"):
            if not item.select_one("td"):
                break
            ip = item.select_one("td").text
            port = item.select_one("td:nth-of-type(2)").text
            proxies.append(f"{ip}:{port}")
        return proxies
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def validate_proxy(proxy):
    """Valida si el proxy funciona conectándose a una página de prueba."""
    try:
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={"http": proxy, "https": proxy},
            timeout=5,
            verify=False
        )
        if response.status_code == 200:
            return True
    except Exception:
        pass
    return False

def create_proxy_driver(PROXY):
    """Crea una instancia de WebDriver con un proxy especificado."""
    options = Options()
    options.add_argument(f'--proxy-server={PROXY}')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Configuración de capacidades usando options.to_capabilities()
    capabilities = options.to_capabilities()

    # Crear WebDriver con capacidades actualizadas
    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )
    return driver

def get_content(ALL_PROXIES):
    """Accede a un sitio web utilizando proxies y realiza scraping."""
    while True:
        if not ALL_PROXIES:
            print("Fetching new proxies...")
            ALL_PROXIES = filter_proxies()
            if not ALL_PROXIES:
                print("No proxies available. Exiting.")
                break

        proxy = ALL_PROXIES.pop()
        print(f"Using proxy: {proxy}")

        if not validate_proxy(proxy):
            print(f"Invalid proxy: {proxy}")
            continue

        driver = None
        try:
            driver = create_proxy_driver(proxy)
            driver.get(link)
            print("Successfully accessed the link")
            # Aquí iría el scraping adicional
            driver.quit()
        except Exception as e:
            print(f"Error: {e}")
            if driver:
                driver.quit()
            continue

if __name__ == '__main__':
    ALL_PROXIES = filter_proxies()
    if not ALL_PROXIES:
        print("No proxies fetched. Exiting.")
    else:
        get_content(ALL_PROXIES)
