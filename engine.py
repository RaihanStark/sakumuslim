import requests
import datetime
from datetimerange import DateTimeRange
import json
import math
import pytz

def get_hijri(timezone):
    r = requests.get('http://api.aladhan.com/v1/gToH?date='+datetime.datetime.now(pytz.timezone(timezone)).strftime('%d-%m-%Y')).json()
    return r['data']['hijri']['day'] +' '+ r['data']['hijri']['month']['en'] + ' ' + r['data']['hijri']['year']

def waktu_tersisa(hour, minute,timezone):
    now = datetime.datetime.now(pytz.timezone(timezone))
    target = pytz.timezone(timezone).localize(datetime.datetime(*now.timetuple()[0:3], hour, minute))
    if target < now:  # if the target is before now, add one day
        target += datetime.timedelta(days=1)

    diff = target - now 
    
    hasil = math.ceil(diff.seconds/60) # Dalam Menit
    if hasil > 60:
        hasil = str(math.ceil(hasil/60))+" Jam Lagi" # Dalam Jam
    else:
        hasil = str(hasil)+" Menit Lagi" # Menit
    return hasil

def current_pray(kota,timezone):
    jadwal = get_jadwal(kota)
    print(jadwal)
    jam = datetime.datetime.now(pytz.timezone(timezone)).time().strftime('%H:%M')
    subuh = DateTimeRange(jadwal['jadwal']['data']['subuh'],jadwal['jadwal']['data']['dzuhur'])
    dzuhur = DateTimeRange(jadwal['jadwal']['data']['dzuhur'], jadwal['jadwal']['data']['ashar'])
    ashar = DateTimeRange(jadwal['jadwal']['data']['ashar'], jadwal['jadwal']['data']['maghrib'])
    magrib = DateTimeRange(jadwal['jadwal']['data']['maghrib'],jadwal['jadwal']['data']['isya'])

    if jam in subuh:
        return('Subuh')
    elif jam in dzuhur:
        return("Dzuhur")
    elif jam in ashar:
        return("Ashar")
    elif jam in magrib:
        return("Maghrib")
    else:
        return("Isya")



def split_jam(jam):
    # H:M
    return jam.split(':')

def solat_berikutnya(kota,timezone):
    jadwal = get_jadwal(kota)
    sekarang = current_pray(kota,timezone)
    
    if sekarang == "Subuh":
        waktuberikutnya = split_jam(jadwal['jadwal']['data']['dzuhur'])
        waktutersisa = waktu_tersisa(int(waktuberikutnya[0]),int(waktuberikutnya[1]),timezone)
        solatberikutnya = "Dzuhur"
    
    elif sekarang == "Dzuhur":
        waktuberikutnya = split_jam(jadwal['jadwal']['data']['ashar'])
        waktutersisa = waktu_tersisa(int(waktuberikutnya[0]),int(waktuberikutnya[1]),timezone)
        solatberikutnya = "Ashar"
    
    elif sekarang == "Ashar":
        waktuberikutnya = split_jam(jadwal['jadwal']['data']['maghrib'])
        waktutersisa = waktu_tersisa(int(waktuberikutnya[0]),int(waktuberikutnya[1]),timezone)
        solatberikutnya = "Maghrib"
    
    elif sekarang == "Maghrib":
        waktuberikutnya = split_jam(jadwal['jadwal']['data']['isya'])
        waktutersisa = waktu_tersisa(int(waktuberikutnya[0]),int(waktuberikutnya[1]),timezone)
        solatberikutnya = "Isya"
    
    elif sekarang == "Isya":
        waktuberikutnya = split_jam(jadwal['jadwal']['data']['subuh'])
        waktutersisa = waktu_tersisa(int(waktuberikutnya[0]),int(waktuberikutnya[1]),timezone)
        solatberikutnya = "Subuh"
        
    return {
        'tersisa':waktutersisa,
        'waktuberikutnya':solatberikutnya
    }




def get_random_ayat():
    # 114 Surat
    # 6236 Ayat
    r = requests.get('https://api.banghasan.com/quran/format/json/acak').json()
    
    return {'arab':r['acak']['ar']['teks'],
            'terjemah':r['acak']['id']['teks'].replace('\n',''),
            'surah':r['surat']['nama'],
            'arti':r['surat']['arti'],
            'ayat':r['acak']['id']['ayat']}

def get_city(city):
    """Menambil Kode Kota
    
    Arguments:
        city {str} -- nama kota
    
    Returns:
        json -- Kode Kota
    """ 
    try:
        r = requests.get('https://api.banghasan.com/sholat/format/json/kota/nama/'+city)
        return r.json()['kota'][0]['id']
    except:
        return 404

def get_jadwal(namakota):
    """Mendapatkan Jadwal Shalat
    
    Arguments:
        kode {str} -- nama kota
    
    Returns:
        json -- jadwal shalat
    """
    kode = get_city(namakota)
    r = requests.get('https://api.banghasan.com/sholat/format/json/jadwal/kota/%s/tanggal/%s'%(kode, str(datetime.date.today())))
    return r.json()

if __name__ == "__main__":
    print(get_jadwal())