from ds.sort_search import mergesort, binary_search
from ds.heap_pq import PriorityQueue
import time
from io_utils import load_drugs
from ds.trie import Trie

kasa = 0

pq = PriorityQueue()
teslimler = []

drug_map = load_drugs()

trie = Trie()
for ilac_adi in drug_map.keys():
    trie.insert(ilac_adi)

print("Yüklenen ilaçlar:", list(drug_map.keys()))

while(True):

    print("\n=== ANA MENÜ ===\n")

    print("1 - Askıda İlaç")
    print("2 - Nöbetçi Eczane")
    print("3 - Çıkış\n")

    secim = input("Seçiminizi tuşlayınız: ")

    if secim == "1":
        
        print("\nAskıda İlaç menüsüne girildi.\n")

        while(True):

            print("1 - Bağış yap")
            print("2 - İlaç sırasına gir")
            print("3 - Son teslimleri gör")
            print("4 - Sırayı görüntüle")
            print("5 - Geri dön\n")

            secim2 = input("Lütfen seçiminizi tuşlayınız: ")

            if secim2 == "1":

                print("\nBağış seçildi\n")

                miktar = int(input("Bağış miktarını TL cinsinden giriniz: "))
                kasa = kasa + miktar

                print("\nBağış işleminiz başarıyla gerçekleştirildi.")
                print("\nKasadaki toplam para: {} TL'dir\n".format(kasa))
                
                if len(pq) == 0:
                    print("Sırada bekleyen yok")
                
                else:
                    teslim_sayisi = 0
                    MAX_TESLIM = 5

                    while len(pq) > 0 and (teslim_sayisi < MAX_TESLIM):
                        hasta = pq.peek() # en öncelikli kişi
                        wait_minutes = int((time.time() - hasta["created_at"]) // 60)
                        hasta["priority"] = (100 * hasta["is_emergency"] + wait_minutes + drug_map[hasta["ilac"]]["criticality"])

                        hangi_ilac = hasta["ilac"]
                        fiyat = drug_map[hangi_ilac]["price"]

                        if kasa >= fiyat:
                            teslim_edilen = pq.pop() # ilk kişiyi sıradan çıkart
                            kasa = kasa - fiyat

                            teslimler.append([teslim_edilen["ad"], teslim_edilen["tc"], teslim_edilen["ilac"],fiyat]) 
                            #'teslim kaydı [ad, tc, ilaç, fiyat]

                            print("Teslim yapıldı ->",teslim_edilen["ad"],"-", teslim_edilen["ilac"])
                            teslim_sayisi = teslim_sayisi + 1
                    
                        else:
                            break
                    
                    if teslim_sayisi == MAX_TESLIM:
                        print("\nTeslim kotası doldu (5/5). Kalanlar bir sonraki bağışı bekliyor\n")
                     
                    if teslim_sayisi == 0:
                        print("\nKasadaki bakiye yetersiz. Sıradaki ilacın fiyatı:",fiyat,"TL'dir\n")
                    
                    else:
                        print("\nToplam teslim sayısı:",teslim_sayisi)
                        print("\nKalan kasa:",kasa,"TL'dir\n")

            elif secim2 == "2":

                print("\nİlaç sırasına girme seçildi\n")

                ad_soyad = input("Ad soyad giriniz: ")
                tc = input("TC giriniz: ")

                acil = input("\nAciliyet olarak önceliğiniz var mı? (E/H)")

                acil = acil.strip().upper()
                is_emergency = 1 if acil == "E" else 0

                
                print("\nMevcut ilaçlar:\n")

                for ilac_adi, info in drug_map.items():
                    print(ilac_adi, "-", "(", info["price"], "TL )")

                prefix = input("\nİlaç arama (en az 1 harf yazın): ").strip()

                oneriler = trie.starts_with(prefix, limit=5)

                if not oneriler:
                    print("\nBu harfle başlayan ilaç yok.")
                    continue

                print("\nÖneriler:")
                
                for i, ad_ilac in enumerate(oneriler, start=1):
                    print(i, "-", ad_ilac)

                sec = input("\nSeçmek için numara yaz (iptal için Enter): ").strip()
                
                if sec == "":
                    continue

                sec_no = int(sec)
                
                if sec_no < 1 or sec_no > len(oneriler):
                    print("\nHatalı seçim.")
                    continue

                hangi_ilac = oneriler[sec_no - 1]

                # büyük/küçük harf fark etmesin diye
                secim_norm = hangi_ilac.strip().lower()
                
                for gerçek_isim in drug_map.keys():
                    
                    if gerçek_isim.lower() == secim_norm:
                        hangi_ilac = gerçek_isim
                        break


                print("\nSeçilen ilaç:", hangi_ilac)
                
                created_at = time.time()

                wait_minutes = int((time.time() - created_at) // 60)

                priority = 100 * is_emergency + wait_minutes + drug_map[hangi_ilac]["criticality"]

                request = {"ad": ad_soyad,"tc": tc,"ilac": hangi_ilac,"is_emergency": is_emergency,"created_at": created_at,"priority": priority}

                pq.push(request)

                print("\nSıraya eklendiniz (heap).")
                print("Öncelik puanınız:", priority)
                print("Bekleyen kişi sayısı:", len(pq), "\n")

            elif secim2 == "3":

                print("\nSon teslimler seçildi\n")
                
                print("SON TESLİMLER\n")

                if len(teslimler) == 0:
                    print("Henüz teslim gerçekleşmedi\n")
                
                else:
                    print("1 - Normal Listele")
                    print("2 - TC'ye göre sırala (MergeSort)")
                    print("3 - TC ile teslim ara (Binary Search)\n")

                    alt = input("Seçiminizi tuşlayınız:")

                    if alt == "1":
                        for t in teslimler:
                            print("\nAd Soyad:",t[0],"TC:",t[1],"İlaç:",t[2],"Fiyat:",t[3],"TL")
                    
                    elif alt == "2":
                        sirali = mergesort(teslimler, key_index=1)
                        for t in sirali:
                            print("\nAd Soyad:",t[0],"TC:",t[1],"İlaç:",t[2],"Fiyat:",t[3],"TL")
                    
                    elif alt == "3":
                        tc_ara = input("\nTC giriniz:")
                        sirali = mergesort(teslimler, key_index=1)
                        sonuc = binary_search(sirali, tc_ara)

                        if sonuc:
                            print("\nBULUNDU →", sonuc)
                        else:
                            print("\nBu TC ile teslim bulunamadı")
            
            elif secim2 == "4":

                print("\nSIRA (HEAP) DURUMU\n")
                print("Bekleyen kişi sayısı:",len(pq))
                print()

            elif secim2 == "5":
                break
            
            else:
                print("\nGeçersiz seçim!\n")

    elif secim == "2":
        print("Nöbetçi Eczane menüsüne girildi.\n")
        print("NÖBETÇİ ECZANELER\n")

        nobetci_eczaneler = ["Taner Eczanesi - 0216 418 94 86","Sakura Eczanesi - 0532 430 02 59","Kadıköy Çarşı Eczanesi - 0216 338 48 38"]
        
        for eczane in nobetci_eczaneler:
            print(eczane)
            print()

    elif secim == "3":
        print("Program sonlanıyor...")
        break
    else:
        print("\nGeçersiz tuşlama yaptınız! Tekrar deneyiniz.")
