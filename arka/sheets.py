import gspread
from gspread.cell import Cell
from gspread.worksheet import Worksheet
import re

from typing import Union

from .date import getTodayDate

gc = gspread.service_account(filename="service_account.json")
sheet = gc.open_by_key("1OqR2Bt7KQiojLqI_Jk74E3Z_DxiV264W4EvOn5tLRpA")
wsAnggota = sheet.worksheet("Daftar Anggota")
wsAbsensi = sheet.worksheet("Absensi")

def getAnggota(id: Union[int, None] = None) -> Union[list, dict]:
    # Column 2: Nama
    # Column 3: Kelas
    # Column 4: Nomor telepon
    # Column 5: Divisi
    # Column 6: ID kartu

    if id:
        siswa = findString(str(id), strict=True)
        if not siswa: return {"message": "Siswa tidak ditemukan"}, 404
        nama = wsAnggota.cell(siswa.row, 2).value
        kelas = wsAnggota.cell(siswa.row, 3).value
        number = wsAnggota.cell(siswa.row, 4).value
        divisi = wsAnggota.cell(siswa.row, 5).value
        id = wsAnggota.cell(siswa.row, 6).value

        return {
            "nama": nama,
            "kelas": kelas,
            "number": number,
            "divisi": divisi,
            "id": id
        }

    rawList = wsAnggota.get_all_values()
    siswa = []
    for list in rawList[1:]:
        siswa.append({
            "nama": list[1],
            "kelas": list[2],
            "number": list[3],
            "divisi": list[4],
            "id": list[5]
        })

    return siswa

def findString(string: str, worksheet: Union[Worksheet, str] = wsAnggota, strict: bool = False) -> Union[Cell, None]:
    if type(worksheet) == str: worksheet = sheet.worksheet(worksheet)

    if strict:
        return worksheet.find(string)
    else:
        regex = re.compile(fr"{string}.*")
        return worksheet.find(regex)

def addAbsensi(id: int, worksheet: Union[Worksheet, str] = wsAbsensi):
    todayDate = getTodayDate()

    headerRowValues = wsAbsensi.row_values(1)
    currentMaxCol = len(headerRowValues)
    maxCol = currentMaxCol
    if headerRowValues[-1] != todayDate:
        maxCol += 1
        wsAbsensi.update_cell(1, maxCol, todayDate)

    siswa = getAnggota(id)
    cariSiswa = findString(siswa["nama"], wsAbsensi, strict=True)
    if wsAbsensi.cell(cariSiswa.row, maxCol).value == "v":
        return {"message": "Siswa sudah absen!"}, 400

    wsAbsensi.update_cell(cariSiswa.row, maxCol, "v")    
    return {"message": f"Berhasil absensi"}
