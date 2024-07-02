from lib.helper.helper import *  # Mengimpor semua fungsi dan variabel dari modul helper
from datetime import datetime  # Mengimpor modul datetime untuk mendapatkan waktu saat ini

# Tambahkan variabel global untuk menyimpan total pesan CRITICAL
total_critical = 0

class Log:

    @classmethod
    def info(cls, text):
        print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+G+"INFO"+N+"] "+text)

    @classmethod
    def warning(cls, text):
        print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+Y+"WARNING"+N+"] "+text)

    @classmethod
    def high(cls, text):
        global total_critical
        total_critical += 1
        print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+R+"CRITICAL"+N+"] "+text)

    @classmethod
    def generate_report(cls):
        report = f"Total CRITICAL messages: {total_critical}"
        print(report)
        return report
