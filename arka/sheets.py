import gspread
from gspread.cell import Cell
from gspread.worksheet import Worksheet
import re

from typing import Union

gc = gspread.service_account(filename="service_account.json")
sheet = gc.open_by_key("1OqR2Bt7KQiojLqI_Jk74E3Z_DxiV264W4EvOn5tLRpA")
ws = sheet.worksheet("Daftar Anggota")

def getAnggota(id: Union[int, None] = None) -> Union[list, dict]:
    # Column 2: Nama
    # Column 3: Kelas
    # Column 4: Nomor telepon
    # Column 5: Divisi
    # Column 8: ID kartu

    if id:
        siswa = findString(str(id), strict=True)
        if not siswa: return {"message": "Siswa tidak ditemukan"}, 404
        nama = ws.cell(siswa.row, 2).value
        kelas = ws.cell(siswa.row, 3).value
        number = ws.cell(siswa.row, 4).value
        divisi = ws.cell(siswa.row, 5).value
        id = ws.cell(siswa.row, 8).value

        return {
            "nama": nama,
            "kelas": kelas,
            "number": number,
            "divisi": divisi,
            "id": id
        }

    rawList = ws.get_all_values()
    siswa = []
    for list in rawList[1:]:
        siswa.append({
            "nama": list[1],
            "kelas": list[2],
            "number": list[3],
            "divisi": list[4],
            "id": list[7]
        })

    return siswa

def findString(string: str, worksheet: Union[Worksheet, str] = ws, strict: bool = False) -> Union[Cell, None]:
    if type(worksheet) == str: worksheet = sheet.worksheet(worksheet)

    if strict:
        return worksheet.find(string)
    else:
        regex = re.compile(fr"{string}.*")
        return worksheet.find(regex)
