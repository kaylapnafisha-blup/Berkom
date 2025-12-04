def mesin(a,b):
    total = a - b
    if total > 8:
        efisiensi = (total-8)/8*100
    else:
        efisiensi = total/8*100
    return efisiensi

def bijih(a):
    efisiensi = a/20*100
    return efisiensi

def bahan_bakar(a, b, c):
    total = a - b
    if total*c > 20:
        efisiensi = (total*c - 20)/20*100
    else: 
        efisiensi = (total*c)/20*100
    return efisiensi

def total(a, b, c):
    efisien = (a+b+c)/3
    return efisien

def bensin(a,b):
    harga = a*b*20000*365
    return harga

def gaji(a):
    gaji = a*50000*365
    return gaji

def penjualan(a):
    harga = a*1000000*365
    return harga

def laba(a, b):
    hasil = a - b
    return hasil
