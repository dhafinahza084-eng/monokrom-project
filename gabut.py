import pygame
import time
import sys
import tkinter as tk
import tkinter.font as tkfont
import random

KECEPATAN_KETIK = 0.12  # makin besar, makin lambat teks muncul

def ketik(teks):
    for huruf in teks:
        sys.stdout.write(huruf)
        sys.stdout.flush()
        time.sleep(KECEPATAN_KETIK)
    print()

pygame.mixer.init()
pygame.mixer.music.load("monokrom.mp3")
pygame.mixer.music.play()

lirik = [
    (0, "MONOKROM"),

    (7, "Lembaran foto hitam-putih"),
    (12, "Aku coba ingat lagi"),
    (15, "Warna bajumu kala itu"),
    (18, "Kali pertama di hidupku"),
    (23, "Manusia lain memelukku"),
    
    (29, "Lembaran foto hitam-putih"),
    (34, "Aku coba ingat lagi"),
    (36, "Wangi rumah di sore itu"),
    (40, "Kue cokelat, balon warna-warni"),
    (45, "Pesta hari ulang tahunku"),

    (50, "Dimana pun kalian berada"),
    (55.5, "kukirimkan terimakasih"),
    (60.3, "Untuk warna dalam hidupku"),
    (63, "dan banyak kenangan indah"),
    (70, "kau melukis aku"),
    (74, "<3"),
]

root = tk.Tk()
root.title("Lirik")
root.attributes("-topmost", True)
lebar, tinggi = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{lebar}x{tinggi}+0+0")
root.attributes("-fullscreen", True)

canvas = tk.Canvas(root, width=lebar, height=tinggi, bg="#bfeaff", highlightthickness=0)
canvas.pack(expand=True, fill="both")

# Tkinter Canvas tidak menyediakan gradient bawaan, jadi latar dibuat dari pita warna.
warna_atas = (105, 190, 245)
warna_bawah = (255, 239, 196)
jumlah_pita = 160
for indeks in range(jumlah_pita):
    rasio = indeks / (jumlah_pita - 1)
    warna = "#{:02x}{:02x}{:02x}".format(*(
        round(atas + (bawah - atas) * rasio)
        for atas, bawah in zip(warna_atas, warna_bawah)
    ))
    y_awal = tinggi * indeks / jumlah_pita
    y_akhir = tinggi * (indeks + 1) / jumlah_pita
    canvas.create_rectangle(0, y_awal, lebar, y_akhir, fill=warna, outline=warna)

# Lapisan halo membuat cahaya matahari tampak menyebar lembut.
matahari_x, matahari_y = lebar * 0.82, tinggi * 0.2
ukuran_matahari = min(lebar, tinggi) * 0.045
for skala, warna, pola in (
    (3.2, "#fff8d8", "gray12"),
    (2.5, "#fff4c2", "gray25"),
    (1.8, "#fff0ad", "gray50"),
):
    canvas.create_oval(
        matahari_x - ukuran_matahari * skala,
        matahari_y - ukuran_matahari * skala,
        matahari_x + ukuran_matahari * skala,
        matahari_y + ukuran_matahari * skala,
        fill=warna,
        stipple=pola,
        outline="",
    )
canvas.create_oval(
    matahari_x - ukuran_matahari,
    matahari_y - ukuran_matahari,
    matahari_x + ukuran_matahari,
    matahari_y + ukuran_matahari,
    fill="#ffe08a",
    outline="#fff3bf",
    width=3,
)

root.bind("<Escape>", lambda event: root.destroy())

awan = []
bentuk_awan = [
    (0.18, 0.67, 0.22, 0.32),
    (0.38, 0.48, 0.25, 0.46),
    (0.62, 0.44, 0.26, 0.52),
    (0.82, 0.66, 0.20, 0.32),
    (0.50, 0.74, 0.44, 0.25),
]

for _ in range(18):
    lebar_awan = random.randint(90, 180)
    tinggi_awan = random.randint(38, 64)
    x = random.randint(-60, lebar)
    y = random.randint(-100, tinggi)
    warna = random.choice(("#ffffff", "#f7fbff", "#fffdf5"))
    bagian = []

    for tengah_x, tengah_y, radius_x, radius_y in bentuk_awan:
        bagian.append(canvas.create_oval(
            x + (tengah_x - radius_x) * lebar_awan,
            y + (tengah_y - radius_y) * tinggi_awan,
            x + (tengah_x + radius_x) * lebar_awan,
            y + (tengah_y + radius_y) * tinggi_awan,
            fill=warna,
            outline=warna,
        ))

    awan.append({
        "bagian": bagian,
        "x": x,
        "y": y,
        "lebar": lebar_awan,
        "tinggi": tinggi_awan,
        "kecepatan": random.uniform(0.7, 1.8),
    })

font_teks = tkfont.Font(root=root, family="Terminal", size=34, weight="bold")
jarak_huruf = -1
lapisan_garis = (
    (-2, -2), (0, -2), (2, -2),
    (-2, 0),             (2, 0),
    (-2, 2),  (0, 2),   (2, 2),
)


def lebar_baris(teks):
    return sum(font_teks.measure(huruf) for huruf in teks) + jarak_huruf * max(0, len(teks) - 1)


def pecah_baris(teks):
    hasil = []
    baris = ""
    for kata in teks.split():
        calon = f"{baris} {kata}".strip()
        if baris and lebar_baris(calon) > lebar - 100:
            hasil.append(baris)
            baris = kata
        else:
            baris = calon
    if baris:
        hasil.append(baris)
    return hasil


def siapkan_teks(teks):
    tinggi_baris = font_teks.metrics("linespace")
    baris_teks = pecah_baris(teks)
    y_awal = tinggi / 2 - (len(baris_teks) - 1) * tinggi_baris / 2
    karakter = []

    for nomor_baris, baris in enumerate(baris_teks):
        x = (lebar - lebar_baris(baris)) / 2
        y = y_awal + nomor_baris * tinggi_baris
        for huruf in baris:
            lebar_huruf = font_teks.measure(huruf)
            tengah_x = x + lebar_huruf / 2
            bayangan = canvas.create_text(
                tengah_x + 4,
                y + 4,
                text=huruf,
                font=font_teks,
                fill="#24516f",
                state="hidden",
            )
            lapisan = [
                canvas.create_text(
                    tengah_x + dx,
                    y + dy,
                    text=huruf,
                    font=font_teks,
                    fill="#17476b",
                    state="hidden",
                )
                for dx, dy in lapisan_garis
            ]
            depan = canvas.create_text(
                tengah_x,
                y,
                text=huruf,
                font=font_teks,
                fill="white",
                state="hidden",
            )
            karakter.append((bayangan, lapisan, depan, x + lebar_huruf, y))
            x += lebar_huruf + jarak_huruf

    return karakter


karakter_teks = []
kursor_teks = None
panel_teks = None
generasi_ketikan = 0


def ketik_teks(teks, selesai):
    global karakter_teks, kursor_teks, panel_teks, generasi_ketikan
    generasi_ketikan += 1
    generasi = generasi_ketikan
    for bayangan, lapisan, depan, _, _ in karakter_teks:
        for item in (bayangan, *lapisan, depan):
            canvas.delete(item)
    if panel_teks is not None:
        canvas.delete(panel_teks)

    karakter_teks = siapkan_teks(teks)
    baris_teks = pecah_baris(teks)
    lebar_panel = max(lebar_baris(baris) for baris in baris_teks)
    tinggi_baris = font_teks.metrics("linespace")
    tinggi_panel = len(baris_teks) * tinggi_baris
    panel_teks = canvas.create_rectangle(
        lebar / 2 - lebar_panel / 2 - 32,
        tinggi / 2 - tinggi_panel / 2 - 32,
        lebar / 2 + lebar_panel / 2 + 32,
        tinggi / 2 + tinggi_panel / 2 + 32,
        fill="#397da5",
        stipple="gray25",
        outline="#d9f1ff",
        width=3,
    )
    canvas.tag_lower(panel_teks, karakter_teks[0][0])

    if kursor_teks is not None:
        for pixel in kursor_teks:
            canvas.delete(pixel)

    posisi_awal = karakter_teks[0]
    lebar_pixel = 5
    tinggi_bagian = 12
    jarak_bagian = 8
    tinggi_kursor = tinggi_bagian * 2 + jarak_bagian
    kursor_teks = [
        canvas.create_rectangle(
            posisi_awal[3] + 4,
            posisi_awal[4] - tinggi_kursor / 2 + indeks_bagian * (tinggi_bagian + jarak_bagian),
            posisi_awal[3] + 4 + lebar_pixel,
            posisi_awal[4] - tinggi_kursor / 2 + indeks_bagian * (tinggi_bagian + jarak_bagian) + tinggi_bagian,
            fill="white",
            outline="white",
        )
        for indeks_bagian in range(2)
    ]
    indeks = 0
    kursor_terlihat = True

    def kedip_kursor():
        nonlocal kursor_terlihat
        if generasi != generasi_ketikan:
            return
        kursor_terlihat = not kursor_terlihat
        for pixel in kursor_teks:
            canvas.itemconfig(
                pixel,
                state="normal" if kursor_terlihat else "hidden",
            )
        root.after(400, kedip_kursor)

    def tampilkan_huruf():
        nonlocal indeks, kursor_terlihat
        if generasi != generasi_ketikan:
            return
        if indeks >= len(karakter_teks):
            for pixel in kursor_teks:
                canvas.itemconfig(pixel, state="hidden")
            selesai()
            return

        bayangan, lapisan, depan, x_akhir, y = karakter_teks[indeks]
        for item in (bayangan, *lapisan, depan):
            canvas.itemconfig(item, state="normal")
        for indeks_bagian, pixel in enumerate(kursor_teks):
            y_atas = y - tinggi_kursor / 2 + indeks_bagian * (tinggi_bagian + jarak_bagian)
            canvas.coords(
                pixel,
                x_akhir + 4,
                y_atas,
                x_akhir + 4 + lebar_pixel,
                y_atas + tinggi_bagian,
            )
            canvas.itemconfig(pixel, state="normal")
        kursor_terlihat = True
        indeks += 1
        root.after(45, tampilkan_huruf)

    kedip_kursor()
    tampilkan_huruf()


def gerakkan_awan():
    for gumpal in awan:
        gumpal["y"] -= gumpal["kecepatan"]

        if gumpal["y"] + gumpal["tinggi"] < 0:
            gumpal["x"] = random.randint(-60, lebar)
            gumpal["y"] = tinggi + random.randint(20, 180)

        for item, (tengah_x, tengah_y, radius_x, radius_y) in zip(
            gumpal["bagian"], bentuk_awan
        ):
            canvas.coords(
                item,
                gumpal["x"] + (tengah_x - radius_x) * gumpal["lebar"],
                gumpal["y"] + (tengah_y - radius_y) * gumpal["tinggi"],
                gumpal["x"] + (tengah_x + radius_x) * gumpal["lebar"],
                gumpal["y"] + (tengah_y + radius_y) * gumpal["tinggi"],
            )

    root.after(40, gerakkan_awan)


gerakkan_awan()

mulai = time.monotonic()

def tampilkan(index=0):
    if index >= len(lirik):
        return

    timestamp, teks = lirik[index]
    jeda = max(0, int((timestamp - (time.monotonic() - mulai)) * 1000))

    def perbarui():
        ketik_teks(teks, lambda: tampilkan(index + 1))

    root.after(jeda, perbarui)

tampilkan()
root.mainloop()