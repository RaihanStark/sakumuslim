from flask import Flask, url_for, render_template, request
from engine import *

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Get City
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    r = requests.get('http://ip-api.com/json/{}'.format(ip))
    lokasi = r.json()
    print(ip)
    print(lokasi)
    kota = lokasi['city']
    timezone = lokasi['timezone']
    return render_template('dashboard.html', 
                           tanggalhijriyah=get_hijri(timezone),
                           jadwalsolat=get_jadwal(kota),
                           quran=get_random_ayat(),
                           waktusolat=current_pray(kota,timezone),
                           solatberikutnya=solat_berikutnya(kota,timezone),
                           namakota=kota)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")