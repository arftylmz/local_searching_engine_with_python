from tkinter import *
import os
import re
import shelve
import time

class Editor(Frame):

    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.root=parent
        self.initUI()

    def initUI(self):
        # listbox listemiz ve veri tabanı tablolarımız başlangıçta oluşturuluyor
        self.liste = ["Düz Metin","Program Kodu"]
        self.dbtables = {'kelime_lokasyon': 'kelime_lokasyon.db',
                    'zaman_sozluk': 'zaman_sozluk.db',
                    'index': 'index.db'}
        self.degerler = {}
        self.grid()
        frame = Frame(self, bg="Beige", width="650", height="700", pady="25", padx="10")
        frame.grid()



        #Başlık
        self.Baslik = Label(frame, text="Dosya Arayici", fg="Blue", bg="Beige")
        self.Baslik.config(font=("Courier", 16, "bold"))
        self.Baslik.grid(row=0, column=2,sticky = N)

        self.boslabel = Label(frame, text="", fg="Blue", bg="Beige")
        self.boslabel.grid(row=1, column=0, columnspan=6)
        # dizinin girileceği ve derinliğin belirleneceği bölüm aynı zamanda indexleme işlemi burada oluşuyor
        self.dizin_text = Label(frame, text="Baslangic dizini: ", fg="Blue", bg="Beige")
        self.dizin_text.config(font=("Courier", 12, "bold italic"))
        self.dizin_text.grid(row=2, column=0)

        self.dizin_degeri = StringVar()
        self.dizin = Entry(frame, font="Times 13" ,width=30,bg="Beige",textvariable = self.dizin_degeri)
        self.dizin.grid(row=2, column=2,columnspan = 2,sticky = N)

        self.dizin = Label(frame, text="Derinlik: ", fg="Blue", bg="Beige")
        self.dizin.config(font=("Courier", 12, "bold italic"))
        self.dizin.grid(row=3, column=0,sticky = S + W + E + N)


        self.Index_button = Button(frame, text="İndex Olustur", fg="Blue", bg="Gold",width=25,command = self.indexle)
        self.Index_button.grid(row=3, column=2,columnspan = 2,sticky = S )
        # indeksleme belirteci
        self.animasyon_label = Label(frame,text="" ,fg="Blue", bg="Beige")
        self.animasyon_label.grid(row=3, column=4)

        self.derinlik_degeri = IntVar()
        self.derinlik_entry = Entry(frame, font="Times 13", width=3, bg="Beige", textvariable=self.derinlik_degeri)
        self.derinlik_entry.grid(row=3, column=0, sticky=E)

        self.boslabel = Label(frame, text="",fg="Blue", bg="Beige")
        self.boslabel.grid(row=4, column=0, columnspan=6)

        # arama kelimesi
        self.aranacak_kelime = StringVar()
        self.arama_entry = Entry(frame, font="Times 13", width=30, bg="Beige", textvariable=self.aranacak_kelime)
        self.arama_entry.grid(row=5, column=1,columnspan = 2, sticky=E)

        #Bazı arama ayarları
        self.Siralama_Label = Label(frame, text="Siralama Kriteri", fg="Blue", bg="Beige")
        self.Siralama_Label.config(font=("Courier", 14, "bold italic"))
        self.Siralama_Label.grid(row=6, column=0,sticky=E)

        self.kriter = IntVar()
        self.kriter2 = IntVar()
        self.radio1 = Checkbutton(frame, text="Kelime Uzakligi", variable=self.kriter , fg="Blue", bg="Beige")
        self.radio2 = Checkbutton(frame, text="Erisim \n Kriteri", variable=self.kriter2 , fg="Blue", bg="Beige")
        self.radio1.select()
        self.radio2.select()
        self.radio1.grid(row=7, column=0, sticky=W, padx="30")
        self.radio2.grid(row=8, column=0, sticky=W, padx="30")

        self.Agirlik_Label = Label(frame, text="Agirlik", fg="Blue", bg="Beige")
        self.Agirlik_Label.config(font=("Courier", 14, "bold italic"))
        self.Agirlik_Label.grid(row=6, column=1, sticky=E)

        self.kelime_uzakligi_agirlik_degeri = IntVar()
        self.kelime_uzakligi_agirlik_degeri.set(1)
        self.uzaklik_text = Entry(frame, font="Times 13", width=3, bg="Beige", textvariable=self.kelime_uzakligi_agirlik_degeri)
        self.uzaklik_text.grid(row=7, column=1, sticky=N + E,padx = 30)

        self.erisim_zamani_agirlik_degeri = IntVar()
        self.erisim_zamani_agirlik_degeri.set(1)
        self.erisim_text = Entry(frame, font="Times 13", width=3, bg="Beige", textvariable=self.erisim_zamani_agirlik_degeri)
        self.erisim_text.grid(row=8, column=1, sticky=S + E, padx=30)

        self.Filtre_Label = Label(frame, text="Filtre", fg="Blue", bg="Beige")
        self.Filtre_Label.config(font=("Courier", 14, "bold italic"))
        self.Filtre_Label.grid(row=6, column=2, sticky=E)

        self.listbox = Listbox(frame, height=3,width = 20, selectmode=MULTIPLE, fg="Blue", bg="Beige")
        self.listbox.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox.grid(row=7, column=2,rowspan = 3, sticky=E)
        self.listbox.insert(END,"Düz Metin")
        self.listbox.insert(END,"Program Kodu")
        self.listbox.select_set(0,END)

        self.Ara_Button = Button(frame, text="Ara", fg="Blue", bg="Gold", width=15,command = self.arama)
        self.Ara_Button.grid(row=7, column=4, columnspan=2, sticky=S)

        #Arama verilerinin yazıldığı text
        self.Arama_Verileri = Text(frame ,height=15,width=40,bg="Beige",font=("Times 13", 9))
        self.Arama_Verileri.tag_configure("italic", font="Times 13" )
        self.Arama_Verileri.grid(row=10, column=0, columnspan=4, sticky=W + E)
        self.Arama_Verileri_scroll = Scrollbar(frame, orient=VERTICAL, width=35)
        self.Arama_Verileri_scroll.config(command=self.Arama_Verileri.yview)
        self.Arama_Verileri_scroll.grid(row=10, column=4, sticky=N + S + W)

        # sayfalama buttonlar fakat çalışmıyor
        self.Sonraki_button = Button(frame, text="Sonraki", fg="Blue", bg="Gold", width=10,command=self.arttır)
        self.Sonraki_button.grid(row = 11,column = 4)

        self.Onceki_button = Button(frame, text="Onceki", fg="Blue", bg="Gold", width=10,command=self.azalt)
        self.Onceki_button.grid(row=11, column=3)
        self.a=0
        self.sayfanin_sayisi = IntVar()
        self.sayfa_sayisi = Label(frame, fg="Blue", bg="Beige",textvariable=self.sayfanin_sayisi)
        self.sayfa_sayisi.config(font=("Courier", 12, "bold italic"))
        self.sayfa_sayisi.grid(row = 11,column = 2,sticky = E)
        self.bosliste=[]
        self.bosliste2=[]


    def arttır(self):
        if self.a==10:
            return -1
        self.a+=1
        self.Arama_Verileri.delete(1.0, END)
        if self.a==1:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[10:20])
        elif self.a==2:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[20:30])
        elif self.a==3:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[30:40])
        elif self.a==4:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[40:50])
        elif self.a==5:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[50:60])
        elif self.a==6:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[60:70])
        elif self.a==7:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[70:80])
        elif self.a==8:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[80:90])
        elif self.a==9:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[90:100])
        elif self.a==10:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[100:110])
        self.sayfanin_sayisi.set(self.a)
        self.update_idletasks()
    def azalt(self):
        if self.a ==0:
            return -1
        self.a=self.a-1
        self.Arama_Verileri.delete(1.0, END)
        if self.a==0:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[0:10])
        if self.a==1:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[10:20])
        elif self.a==2:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[20:30])
        elif self.a==3:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[30:40])
        elif self.a==4:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[40:50])
        elif self.a==5:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[50:60])
        elif self.a==6:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[60:70])
        elif self.a==7:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[70:80])
        elif self.a==8:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[80:90])
        elif self.a==9:
            self.Arama_Verileri.insert(INSERT,self.bosliste2[90:100])
        self.sayfanin_sayisi.set(self.a)
        self.update_idletasks()


    def animate(self, i):
        # Animasyonu yapıyoruz ( . . . . . )
        self.animasyon_label.config(text=f"( {'..' * i} ) \n indexleme yükleniyor")
        self.update_idletasks()

    def onSelect(self, val):
        try:
            self.liste.clear()
            idx = self.listbox.curselection()
            for i in idx:
                self.value = self.listbox.get(i)
                if self.value not in self.liste:
                    self.liste.append(self.value)

            print(self.liste)
        except:
            print("")


    def indexle(self):

        # kullanıcıya indeks animasyonu sunuyoruz
        a=1
        self.animate(a)
        a += 1
        self.derinlik = self.derinlik_degeri.get()
        self.animate(a)
        a += 1
        self.dizin_ = self.dizin_degeri.get()
        self.animate(a)
        a += 1
        if self.dizin_== "":
            self.animasyon_label.config(text="indexleme başarısız")
            self.Arama_Verileri.delete(1.0, END)
            pass
            self.Arama_Verileri.insert(INSERT,"Lütfen geçerli bir dizin adı giriniz")
            return -1
        self.animate(a)
        a += 1
        # daha önceden yazdığımız crawler sınıfı bize dosyaları dizin hiyerarşisi içinde gezmemizi sağlıyor
        crawler = Crawler(self.dbtables)
        crawler.veri_tabani()
        self.animate(a)
        a += 1
        # burada indeksleme başlıyor
        crawler.crawl(self.dizin_,self.derinlik)
        #veri tabanı burada kapatılıyor. ilerde indekslemede sorun çıkabilir.
        crawler.close()
        self.animasyon_label.config(text="İndexleme tamamlandı")
    def arama(self):
        # arama yapmak için kullanıcıdan aldığımız gerekli değerler burada toplanıyor
        start_time = time.time()
        self.arama_tipi = ""
        self.karar = self.kriter.get()
        self.karar2 = self.kriter2.get()
        self.aranacak = self.aranacak_kelime.get()
        # arama kelime kontrolü
        if self.aranacak == "":
            self.Arama_Verileri.delete(1.0, END)
            self.Arama_Verileri.insert(INSERT, "Lütfen aranacak bir kelime giriniz")
            return -1
        # ağırlık kontrolü
        try:
            self.kelime_uzakligi_agirlik = float(self.kelime_uzakligi_agirlik_degeri.get())
            self.erisim_zamani_agirlik = float(self.erisim_zamani_agirlik_degeri.get())
        except TclError:
            self.Arama_Verileri.delete(1.0, END)
            self.Arama_Verileri.insert(INSERT, "Lütfen Ağırlık değerlerinizi doğru giriniz.")
            return -1


        search = searcher(self.dbtables)
        #sıralama ölçütü kontrolü
        if self.karar == 0 and self.karar2 == 0:
            self.Arama_Verileri.delete(1.0, END)
            self.Arama_Verileri.insert(INSERT, "Lütfen bir sıralama ölçütü seçiniz giriniz")
            return -1
        elif self.karar == 1 and self.karar2 == 0:
            self.arama_tipi = "kelime uzaklığı"

        elif self.karar == 0 and self.karar2 == 1:
            self.arama_tipi = "erişim zamanı"

        else:
            self.arama_tipi = "iki arama ölçütü"
        #geçen zamanı ve dosya sayısını ekrana bastırdığımız yer
        elapsed_time = time.time() - start_time
        self.Arama_Verileri.delete(1.0,END)
        #search sınıfından türettiğimiz obje ile arama işlemini burada yapıyoruz. gelen değerler arama skorlarımızdır
        self.degerler = search.arama(self.aranacak, self.arama_tipi, self.kelime_uzakligi_agirlik, self.erisim_zamani_agirlik)



        #kullanıcı tercihine göre burada ekrana değerleri bastırıyoruz
        self.bosliste2.clear()
        for key in self.degerler:

            if len(self.liste) == 1:
                if self.liste[0] == "Program Kodu":
                    programlama = re.search(".py|.cpp", key)
                    if programlama:
                        puan = str(self.degerler[key])
                        dosya_yolu = str(key)
                        boyut = str(os.stat(dosya_yolu).st_size)
                        # self.Arama_Verileri.insert(INSERT, dosya_yolu + "\t" + boyut + "\t" + puan + "\n")
                        self.Arama_Verileri.delete(1.0, END)
                        self.Arama_Verileri.insert(INSERT, str(len(self.degerler)) + " Dosya " + "( " + str(
                            elapsed_time) + " saniye" + " )" + "\n")
                        self.veri2 = dosya_yolu + "\t" + boyut + "\t" + puan + "\n"
                        self.bosliste2.append(self.veri2)
                        ilk_yazdir = self.bosliste2[0:10]
                        self.Arama_Verileri.insert(INSERT, ilk_yazdir)
                elif self.liste[0] == "Düz Metin":
                    metin = re.search(".txt",key)
                    if metin:
                        puan = str(self.degerler[key])
                        dosya_yolu = str(key)
                        boyut = str(os.stat(dosya_yolu).st_size)
                        # self.Arama_Verileri.insert(INSERT, dosya_yolu + "\t" + boyut + "\t" + puan + "\n")
                        self.Arama_Verileri.delete(1.0, END)
                        self.Arama_Verileri.insert(INSERT, str(len(self.degerler)) + " Dosya " + "( " + str(
                            elapsed_time) + " saniye" + " )" + "\n")
                        self.veri2 = dosya_yolu + "\t" + boyut + "\t" + puan + "\n"
                        self.bosliste2.append(self.veri2)
                        ilk_yazdir = self.bosliste2[0:10]
                        self.Arama_Verileri.insert(INSERT, ilk_yazdir)
            elif len(self.liste) == 2:
                puan = str(self.degerler[key])
                dosya_yolu = str(key)
                boyut = str(os.stat(dosya_yolu).st_size)
                # self.Arama_Verileri.insert(INSERT, dosya_yolu + "\t" + boyut + "\t" + puan + "\n")
                self.Arama_Verileri.delete(1.0, END)
                self.Arama_Verileri.insert(INSERT, str(len(self.degerler)) + " Dosya " + "( " + str(
                elapsed_time) + " saniye" + " )" + "\n")
                self.veri2 = dosya_yolu + "\t" + boyut + "\t" + puan + "\n"
                self.bosliste2.append(self.veri2)
                ilk_yazdir = self.bosliste2[0:10]
                self.Arama_Verileri.insert(INSERT, ilk_yazdir)
            elif len(self.liste) == 0:
                self.Arama_Verileri.delete(1.0, END)
                self.Arama_Verileri.insert(INSERT, "Lütfen Doğru bir dosya kategorisi seçiniz giriniz.")
                return -1





        #veri tabanının kapatılmas. çok önemli açık veri tabanı üzerine crawl işlemi yapılırsa program indekslerini kaybediyor.
        search.close()
    def dene(self):
        pass

class Crawler():
    def __init__(self,dbtables):
        self.dbtables = dbtables
        #kelime lokasyonlarını çektiğimiz fonksiyon
    def get_words(self,kelime_lokasyon,yol,dosya):


        kelime2 = os.path.join(yol, dosya)
        kelime = open(kelime2,"r",encoding='UTF-8').read()
        splitter = re.compile('\\W+')
        dizi = []
        # Split the words by non-alpha characters
        words = [s.lower() for s in splitter.split(kelime)]

        # Return the unique set of words only

        count = 0
        for w in words:
            son = re.compile(r'\n').sub('', w)
            kelime_lokasyon.setdefault(kelime2, {})
            if son in kelime_lokasyon[kelime2]:
                cemal = kelime_lokasyon[kelime2][son]
                dizi = cemal.copy()
                dizi.append(count)
                kelime_lokasyon[kelime2][son] = dizi
            else:

                kelime_lokasyon[kelime2][son] = []
                kelime_lokasyon[kelime2][son].append(count)

            count += 1

        return kelime_lokasyon

    #erişim zamanını çektiğimiz fonksiyon
    def get_erisim_zamani(self,zaman_sozluk,yol,dosya):
        tam_yol = str(os.path.join(yol,dosya))
        dosya_zamani = float(os.stat(tam_yol).st_atime)
        zaman_sozluk[tam_yol] = dosya_zamani
    #indeks oluşturduğumuz fonksiyon
    def index_olustur(self,index,yol,dosya):
        tam_yol = str(os.path.join(yol, dosya))
        index[tam_yol] = 1


    # veri tabanı açma kapatma işlemleri
    def veri_tabani(self):


        self.kelime_lokasyon = shelve.open(self.dbtables['kelime_lokasyon'], writeback=True, flag='c')
        self.zaman_sozluk= shelve.open(self.dbtables['zaman_sozluk'], writeback=True, flag='c')
        self.index = shelve.open(self.dbtables['index'], writeback=True, flag='c')


    def close(self):
        if hasattr(self, 'kelime_lokasyon'): self.kelime_lokasyon.close()
        if hasattr(self, 'zaman_sozluk'): self.zaman_sozluk.close()
        if hasattr(self, 'index'): self.index.close()

    #indeksleme yapıldı mı kontrolü, daha önce indekslenen veriler buraya giremiyor.
    def is_index(self,yol,dosya):

        tam_yol = str(os.path.join(yol, dosya))
        cemal = self.index.get(tam_yol)

        if cemal == None:
            return True
        else:
            if tam_yol == cemal:
                return False

    # dizinlerde hiyerarşik olarak gezme fonksiyonumuz. Şuan için sadece text ve py uzantılı dosyaları indeksliyor. magic modülü
    # her bilgisayarda farklı çalıştığı için daha genel bir arama olsun istedim. Bu yüzden uzantılarla çalıştım.
    # Eksik ama sorunsuz bir program olması istendi, en azsından indeks aşamasının sorunsuzluğu önemli
    def crawl(self,yol,derinlik = 2):


        dosya_sayı = 0


        sayi = len(os.getcwd().split("\\"))
        for i in os.walk(yol):


            derinlik_hesapla = len(i[0].split("\\")) - sayi
            if derinlik_hesapla > derinlik:
                continue
            for yollar in i:
               if yollar == i[0]:
                   #print(j)
                   continue
               for yolu in yollar:

                   dosya = re.search(".txt|.py",yolu)
                   if dosya:
                        dosya_sayı += 1
                        #print(k)
                        degisken = self.is_index(i[0],yolu)
                        if degisken == True:
                            print("indexlendi: " + i[0] + yolu)
                        else:
                            print("daha önce indexlendi")
                            break
                        self.get_words(self.kelime_lokasyon,i[0],yolu)
                        self.get_erisim_zamani(self.zaman_sozluk,i[0],yolu)
                        self.index_olustur(self.index,i[0],yolu)



        #print(str(dosya_sayı) + " Dosya")
        return self.kelime_lokasyon,self.zaman_sozluk,self.index

class searcher():
    #yapıcı fonksiyojnda veritabanı açılır yıkıcı fonksiyonda veritabanı kapanır.
    def __init__(self,dbtables):
        self.dbtables = dbtables
        self.opendb()
    def __del__(self):
        self.close()

    #veri tabanı açma ve kapatma fonksiyonları
    def opendb(self):
        self.kelime_lokasyon = shelve.open(self.dbtables['kelime_lokasyon'], writeback=True, flag='c')
        self.zaman_sozluk= shelve.open(self.dbtables['zaman_sozluk'], writeback=True, flag='c')
        self.index = shelve.open(self.dbtables['index'], writeback=True, flag='c')

    def close(self):
        if hasattr(self, 'kelime_lokasyon'): self.kelime_lokasyon.close()
        if hasattr(self, 'zaman_sozluk'): self.zaman_sozluk.close()
        if hasattr(self, 'index'): self.index.close()

    #uzaklık skorunun tam hesaplandığı yer
    def UzaklikskorHesapla(self,skorlar_sozlugu):

        self.skorlar_sozlugu = skorlar_sozlugu.copy()
        for i in self.skorlar_sozlugu:
            skor_hesaplayıcı = []
            if len(self.skorlar_sozlugu[i]) >= 2:
                for items in self.skorlar_sozlugu[i]:
                    minim = min(self.skorlar_sozlugu[i][items])
                    dizi = self.skorlar_sozlugu[i][items]
                    skor_hesaplayıcı.append(minim)
                    if len(skor_hesaplayıcı) == 1:
                        continue
                    for j in range(len(skor_hesaplayıcı)):
                        if skor_hesaplayıcı[j] > minim :
                            skor_hesaplayıcı.pop(j+1)
                            for k in dizi:
                                if skor_hesaplayıcı[j] < k:
                                    skor_hesaplayıcı.append(k)
                                    minim = k
                                    break
                    #for i in self.skorlar_sozlugu[i][items]:
                    #print(skorlar_sozlugu[i][items])
                    # dizi = skorlar_sozlugu[i][items][0]
                    # a = dizi
                    # skor_hesaplayıcı.append(a)
                    self.skor_olcüt = 0
                    for m in range(len(skor_hesaplayıcı)):

                            for j in range(m+1,len(skor_hesaplayıcı)):
                                self.skor_olcüt= self.skor_olcüt + (skor_hesaplayıcı[j]-skor_hesaplayıcı[m]) - 1
                                #print(self.skor)
                                break
                lokasyon = i

            self.skor[lokasyon] = self.skor_olcüt
            #print(self.skor)
        return self.skor
    # kelime uzaklık ölçütünün normalize edilmiş halde geri çevirdiği yer
    def kelime_uzaklıgı_olcütü(self,sorgu):
        split = sorgu.split(' ')
        skorlar_sozlugu = {}
        for kelime in split:
            for i in self.kelime_lokasyon:
                for items in self.kelime_lokasyon[i]:
                    if kelime == items:
                        skorlar_sozlugu.setdefault(i,{})
                        skorlar_sozlugu[i][kelime] = self.kelime_lokasyon[i][items]

        self.veri = self.UzaklikskorHesapla(skorlar_sozlugu)
        self.skor = self.normalizescores(self.skor, smallIsBetter=True)
        return self.skor
    #Tekli aramalarda lokasyon bilgisi tutar
    def kelime_lokasyonu_hesaplama(self,sorgu):

        for i in self.kelime_lokasyon:
            for items in self.kelime_lokasyon[i]:
                if sorgu == items:
                    minimumskor =min(self.kelime_lokasyon[i][items])
                    #print(self.kelime_lokasyon[i][items])
                    self.skor[i] = minimumskor
        #print(self.skor)
        return self.normalizescores(self.skor, smallIsBetter=True)
    # erişim zamanı skorunu
    def erisim_zamani(self,sorgu):
        for key in self.kelime_lokasyon:
            for item in self.kelime_lokasyon[key]:
                if sorgu == item:
                    self.skor[key] = self.zaman_sozluk[key]
        #print(self.skor)
        self.skor = self.normalizescores(self.skor, smallIsBetter=True)
        return self.skor
    # mysearchengine modülünden alınan normalize etme fonksiyonu
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall = 0.001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            minscore=max(minscore, vsmall)
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    # Arama sorgulanın kullanıcıc istediği değere göre yapan asıl fonksiyon
    def arama(self, sorgu,arama_tipi,kelime_uzakligi_agirlik,erisim_zamani_agirlik):
        self.skor = {}
        self.agirlik = {}
        if arama_tipi == "kelime uzaklığı" :

            split = sorgu.split(' ')
            if len(split) == 1:
                #print(self.kelime_lokasyonu_hesaplama(sorgu))
                self.agirlik = self.kelime_lokasyonu_hesaplama(sorgu)
                #return self.kelime_lokasyonu_hesaplama(sorgu)
                #return self.agirlik
            else:
                #print(self.kelime_uzaklıgı_olcütü(sorgu))
                self.agirlik = self.kelime_uzaklıgı_olcütü(sorgu)
                #return self.agirlik
        elif arama_tipi == "erişim zamanı":
            self.agirlik = self.erisim_zamani(sorgu)
            #return self.agirlik

        elif arama_tipi == "iki arama ölçütü":
            split = sorgu.split(' ')
            if len(split) == 1:
                self.kelime_lokasyonu_hesaplama(sorgu)
            else:
                self.kelime_uzaklıgı_olcütü(sorgu)
            self.agirlik = self.erisim_zamani(sorgu)

        if erisim_zamani_agirlik == 0.0:
            for key in self.agirlik:
                self.agirlik[key] = self.agirlik[key] * kelime_uzakligi_agirlik
            return self.agirlik
        elif kelime_uzakligi_agirlik == 0.0:
            for key in self.agirlik:
                self.agirlik[key] = self.agirlik[key] * erisim_zamani_agirlik
            return self.agirlik
        else:
            for key in self.agirlik:
                self.agirlik[key] = self.agirlik[key] * kelime_uzakligi_agirlik + self.agirlik[key] * erisim_zamani_agirlik
            return self.agirlik


def main():
    root= Tk()
    root.title("Excel-Reader")
    root.geometry("685x540+300+100")
    #konumu ayarlıyoruz ve ekran boyut ayarlamasını kapatıyoruz.
    root.resizable(FALSE,FALSE)
    App = Editor(root)
    root.mainloop()



if __name__ == '__main__':
    main()
