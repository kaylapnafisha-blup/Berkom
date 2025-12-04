def verifikasi(a):
    try:
        a = int(a)
        return a
    except:
        return None

def verifikasi2(a):
    if a < 0:
        return None
    else:
        return a
