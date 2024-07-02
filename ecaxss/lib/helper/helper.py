import requests, json

##### Warna ####### 
N = '\033[0m'  # Reset warna
W = '\033[1;37m'  # Putih
B = '\033[1;34m'  # Biru
M = '\033[1;35m'  # Magenta
R = '\033[1;31m'  # Merah
G = '\033[1;32m'  # Hijau
Y = '\033[1;33m'  # Kuning
C = '\033[1;36m'  # Cyan

##### Styling ######
underline = "\033[4m"  # Garis bawah

##### Default ######
# User-Agent default untuk permintaan HTTP
agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'} 
# Garis panjang untuk memisahkan bagian-bagian output
line = "—————————————————" 

#####################
def session(proxies, headers, cookie):
    """
    Membuat dan mengkonfigurasi sesi requests dengan proxy, header, dan cookie yang diberikan.
    
    Parameters:
    proxies (dict): Proxy yang akan digunakan untuk koneksi HTTP.
    headers (dict): Headers HTTP yang akan digunakan.
    cookie (str): Cookie yang akan digunakan, dalam format JSON.
    
    Returns:
    requests.Session: Sebuah objek session yang dikonfigurasi.
    """
    r = requests.Session()  # Membuat objek session baru
    r.proxies = proxies  # Mengatur proxy untuk sesi
    r.headers = headers  # Mengatur header untuk sesi
    r.cookies.update(json.loads(cookie))  # Memperbarui cookie dalam sesi dengan mengonversi dari format JSON
    return r  # Mengembalikan objek sesi yang dikonfigurasi
