from dialog import SpeechCloudWS, Dialog, ABNF_INLINE
import random
import asyncio
import logging
from pprint import pprint, pformat
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time
import threading

def najdiZastavku (veta, seznam):
  """
  Nalezení existující plzeňské zastávky v promluvě
     Princip: věta se rozdělí na jednotlivá slova, z po sobě jdoucích slov se pak udělají ještě dvojice a trojice (názvy zastávek se mohou skládat z jednoho, dvou nebo tří slov).
     Z těchto slov, dvojic a trojic se pak hledají takové, které se nacházejí i v seznamu zastávek. Naleznou se všechny, ale vrátí se jen první nalezená (do budoucna vylepšit).
  """
  nalezene = []
  pocet = 0
  slova = veta.split()
  
  seznam_lower = []
  for zastavka in seznam:
    seznam_lower.append(zastavka.lower())
  
  seznam = seznam+seznam_lower
  #print(seznam)
  #print(len(slova))
  
  for slovo in slova:
    if slovo in seznam:
      nalezene.append(slovo)
      pocet = pocet+1
  
  dvojice = []
  for i in range(0, len(slova)-1):
    dvojice.append(slova[i]+" "+slova[i+1])
  
  #print(dvojice)
  for x in dvojice:
    if x in seznam:
      nalezene.append(x)
      pocet = pocet+1

  trojice = []
  for i in range(0, len(slova)-2):
    trojice.append(slova[i]+" "+slova[i+1]+" "+slova[i+2])
  
  #print(trojice)
  for x in trojice:
    if x in seznam:
      nalezene.append(x)
      pocet = pocet+1
  
  #print(nalezene)
  return(nalezene)

def get_spoje(z, do, cas):
    """
    Vycucání spojení z webových stránek IDOS (asi ne úplně legální)
    """
    # request
    if cas==0:
        p = {"f":z, "fc":"307003", "t":do, "tc":"307003"}
    else:
        p = {"time":cas,"f":z, "fc":"307003", "t":do, "tc":"307003"}
    page = requests.get("https://idos.idnes.cz/plzen/spojeni/vysledky/", params = p)
    soup = BeautifulSoup(page.content, 'html.parser')

    # všechna spojení
    spojeni = soup.find("div", {"class": "connection-list"}).findAll("div", recursive=False)
    out = []
    for sp in spojeni:
        details = sp.find("div", {"class": "connection-details"})
        if details == None: continue

        # jen ty dulezite informace (start, cil)
        jednotlive = details.findAll("div", {"class": "outside-of-popup"})
        spoj = []

        for j in jednotlive:

            start = j.find("li", {"class": "item active"})
            #print(len(start))
            end = j.find("li", {"class": "item active last"})
            #print(len(end))
            line = j.find("div", {"class": "line-title"})
            #print(line)
            
            data = []
            for i in [start, end]:
                #print(i)
                #print("\n \n")
                data.append([
                    i.find("p", {"class": "station"}).findAll(text=True)[0], # stanice
                    i.find("p", {"class": "reset time"}).findAll(text=True)[0] # čas
                ])

            linka = j.find("span").findAll(text=True)[0]
      
            """
            linky = []
            for i in [line]:
              #print(i)
              #print("\n \n")
              linky.append([
                  i.find("span").findAll(text=True)[0]
              ])
            """
            
            #print(data)
            #print(linka)
            #print(linky)
          
            
            spoj.append([linka, data])
        out.append(spoj)
    return out
    
def time_diff(time1_str, time2_str):
    time1 = datetime.strptime(time1_str, '%H:%M').time()
    time2 = datetime.strptime(time2_str, '%H:%M').time()
    tdelta = datetime.combine(datetime.today(), time2) - datetime.combine(datetime.today(), time1)
    print("time1: "+str(time1)+"    time2: "+str(time2)+"    delta: "+str(tdelta))
    return tdelta.seconds // 60
    
def time_move(time1, time2, direction):
    format_str = '%H:%M'  # format string for 24-hour HH:MM format
    datetime1 = datetime.strptime(time1, format_str)
    datetime2 = datetime.strptime(time2, format_str)
    if direction=="-":
        time_delta = datetime2 - datetime1
        abs_time_delta = abs(time_delta)
        total_minutes = abs_time_delta.total_seconds() // 60
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        if hours == 0:
            return '{:d}:{:02d}'.format(hours, minutes)
        else:
            return '{}:{:02d}'.format(hours, minutes)

    elif direction=="+":
        reference = datetime(1900, 1, 1) # arbitrary reference date
        timedelta1 = datetime.combine(reference, datetime1.time()) - datetime.combine(reference, reference.time())
        timedelta2 = datetime.combine(reference, datetime2.time()) - datetime.combine(reference, reference.time())
        time_sum = timedelta1 + timedelta2
        total_seconds = time_sum.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02d}"

def get_syntezu(spoje, typ):
    aktSpoj = spoje[0]
    print(aktSpoj)
    print(len(aktSpoj))
    print(aktSpoj[0][1][1][0])
    promluva = ""
    if typ=="spojeni":
        promluva="Nyní nastupte do "+aktSpoj[0][0]+", pravidelný odjezd "+aktSpoj[0][1][0][1]+", a vystupte na zastávce "+aktSpoj[0][1][1][0]+"."
        promluva = promluva.replace("Tram", "tramvaje číslo")
        if len(aktSpoj)>1:
            for i in range(1, len(aktSpoj)):
                promluva = promluva + " Tam přestupte na "+aktSpoj[i][0]+", pravidelný odjezd "+aktSpoj[i][1][0][1]+", a vystupte na zastávce "+aktSpoj[i][1][1][0]+"."
        promluva = promluva.replace("Tram", "tramvaj číslo").replace("Trol", "trolejbus číslo").replace("Bus", "autobus číslo")
    
    elif typ=="spojeni_cas":
        promluva = "V čase "+aktSpoj[0][1][0][1]+" nastupte do "+aktSpoj[0][0]+", a vystupte na zastávce "+aktSpoj[0][1][1][0]+"."
        if len(aktSpoj)>1:
            for i in range(1, len(aktSpoj)):
                promluva = promluva + " Tam přestupte na "+aktSpoj[i][0]+", pravidelný odjezd "+aktSpoj[i][1][0][1]+", a vystupte na zastávce "+aktSpoj[i][1][1][0]+"."
        promluva = promluva.replace("Tram", "tramvaj číslo").replace("Trol", "trolejbus číslo").replace("Bus", "autobus číslo")
    
    elif typ=="odjezd":
        promluva="Tramvaj odjíždí v "+aktSpoj[0][1][0][1]+"."
        
    elif typ=="odjezd_now":
        now = datetime.now().time()
        ted = now.strftime('%-k:%M')  # Use '-I' to remove leading zeros from the hour
        rozdil =  time_diff(ted, aktSpoj[0][1][0][1])
        odjezd = ""
        if rozdil == 0:
            odjezd = "právě nyní."
        elif rozdil == 1:
            odjezd = "za jednu minutu."
        elif rozdil == 2:
            odjezd = "za dvě minuty."
        elif rozdil <= 4:
            odjezd = "za "+str(rozdil)+" minuty."
        else:
            odjezd = "za "+str(rozdil)+" minut."
            
        promluva="Nejbližší tramvaj odjíždí "+odjezd
        
    return promluva
    
def tabule():
    kosutka = get_spoje("Technická", "Košutka", 0)
    univerzita = get_spoje("Technická", "Univerzita", 0)
    
    print(kosutka[0])
    print(kosutka[1])
    print(kosutka[2])
    
    print(univerzita[0])
    print(univerzita[1])
    print(univerzita[2])
    
    odjezdy = [kosutka, univerzita]
    
    return odjezdy
    
def repeat_tabule():
    tabule()
    threading.Timer(10.0, repeat_tabule).start()
  


#get_syntezu(get_spoje("Technická", "Jižní předměstí"))

vozidlo = "tramvaj"
smer = "Košutka"
linka = "4"
cas = "5"
zastavky = ["Adelova", "Amfiteátr", "Anglické nábřeží", "Barvínková", "Bazén Slovany", "Belánka", "Bílá Hora", "Bolevec", "Bolevecká náves", "Bolevecký rybník", "Borská pole", "Borský park", "Bory", "Boženy Němcové", "Božkov", "Brněnská", "Brojova", "Bručná", "Bukovec", "Bušovice", "Bušovice, Sedlecko", "CAN Husova", "CAN Skvrňanská", "CAN Tylova", "Cínová", "Čechurov", "Čermákova", "Černice", "Červený Hrádek", "Čisticí stanice", "Daiho", "Divadlo Alfa", "Divadlo J. K. Tyla", "Dobrovského", "Dolní Vlkýš", "Domažlická rondel", "Doubravka", "Doudlevce ETZ", "Dvořákova", "Dýšina, Armaturka", "Dýšina, náves", "Ejpovická", "Fialková", "Folmavská rondel", "Gambrinus", "Generála Lišky", "Gigant", "Goethova", "Goldscheiderova", "Habrmannovo nám.", "Hasičská stanice", "Hlavní nádraží", "Hlavní pošta", "Hodonínská", "Hokejová hala", "Hradiště", "Hřbitov Zátiší", "Hřbitovní", "Husův park", "Chaty", "Chebská", "Chlumek", "Chodské náměstí", "Chotěšov, u kláštera", "Chotěšov, žel. st.", "Chotíkov, u školy", "Chrást, Lidový dům", "Chrást, ZŠ", "Chválenická", "Jasmínová", "Jatky", "Jedlová", "Jízdecká", "Jižní Předměstí", "K Bukové", "K Dráze", "K Losiné", "K Nemocnici", "K Plzenci", "K Prokopávce", "K Radyni", "K Rozvodně", "K Řečišti", "Kalendářní", "Kalikova", "Karla Steinera", "Karlov", "Ke Karlovu", "Ke Kukačce", "Ke Špitálskému lesu", "Komenského", "Konvalinková", "Košutka", "Koterov", "Kovošrot", "Kozolupy, I", "Kozolupy, u Jána", "Krašovská", "Kruhová", "Křimice", "Kyšice", "Lábkova", "Lašitov", "Lékařská fakulta", "Letkov", "Letkov, U Studánky", "Letkov, u zrcadla", "Letkov, V Podlesí", "Letná", "Liliová", "Líně", "Líně, Sulkov", "Litice", "Lobzy", "Lochotínský pavilón", "Luftova zahrada", "Macháčkova", "Majakovského", "Malesice", "Malesická", "Malická", "Malý Bolevec", "Masarykovo náměstí", "Město Touškov", "Mezi Ploty", "Mikulášská", "Mikulášské náměstí", "Mlýnské nábřeží", "Morseova", "Mozartova", "Mrakodrap", "Na Dlouhých", "Na Rozcestí", "Na Rozhraní", "Na Rychtářce", "Na Spojce", "Nad Úhlavou", "Nad Zátiším", "Nádraží Bílá Hora", "Nádraží Skvrňany", "Nádraží Slovany", "Nádraží Valcha", "Nám. Českých bratří", "Nám. Generála Píky", "Náměstí Karla Panušky", "Náměstí Míru", "Náměstí Republiky", "Náves Lhota", "Náves Litice", "Náves Radčice", "NC Borská pole", "NC Černice", "NC Úněšovská", "Nemocnice Bory", "Nemocnice Lochotín", "Nemocnice Privamed", "Nová Hospoda", "Nová Ves", "Nová Ves, u lesa", "Obchodní", "Obchodní rondel", "Okounová", "Olšová", "Opavská", "Orlík", "Otýlie Beníškové", "Palackého náměstí", "Pampelišková", "Panasonic", "Panelárna", "Papírna Bukovec", "Pařížská", "Pekárna", "Petrohrad", "Petřínská", "Pietas", "Plochá dráha", "Plzeňka", "Pod Dubovkou", "Pod Kyjovem", "Pod Záhorskem", "Pod Zámečkem", "Podhájí", "Poliklinika Bory", "Poliklinika Doubravka", "Poliklinika Slovany", "Pošta Francouzská", "Pošta logistika", "Prazdroj", "Prokopova", "Průmyslová", "Přední Skvrňany", "Přeučilova", "Radčice", "Radnice Slovany", "Radobyčice", "Radobyčická", "Radobyčická náves", "Révová", "Rolnické náměstí", "Rondel", "Rozcestí Podhájí", "Rozcestí Újezd", "Říjnová", "Sady Pětatřicátníků", "Samaritská", "Severka", "Severní", "Sídliště Bory", "Sídliště Košutka", "Skautská", "Skvrňany", "Sladová", "Slovanské údolí", "Slovany", "Slupská", "Sokolovská", "Sokolská", "Stadion Lokomotivy", "Staré letiště", "Starý Plzenec", "Starý Plzenec, Bezručova", "Starý Plzenec, Malá Strana", "Starý Plzenec, Nad tratí", "Starý Plzenec, nádraží", "Starý Plzenec, náměstí", "Starý Plzenec, Sedlec", "Starý Plzenec, Sedlec, Školní", "Starý Plzenec, U Mlýna", "Starý Plzenec, u školy", "Starý Plzenec, Vilová čtvrť", "Starý Plzenec, zdrav. stř.", "Stavební stroje", "Stod", "Sulislavská", "Svatojirská", "Světovar", "Šimerova", "Škoda III. brána", "Škoda VIII. brána", "Školy Vejprnická", "Špačková", "Švihovská", "Techmania", "Technická", "Teplárna", "Terezie Brzkové", "Těšínská", "Tleskačova", "Třemošná, Orlík", "Třemošná, sídliště", "Třemošná, u pošty", "Třemošná, ves", "Tylova", "Tyršův most", "Tyršův sad", "U Apolla", "U Astry", "U Bouzků", "U Darebáka", "U Dráhy", "U Družby", "U Duhy", "U Gery", "U Hřbitova", "U Ježíška", "U Kasáren", "U Kondrů", "U Letiště", "U Luny", "U Nové Hospody", "U Panasoniku", "U Pietasu", "U Plynárny", "U Práce", "U Prodejny", "U Přehrady", "U Radbuzy", "U Staré Kovárny", "U Světovaru", "U Synagogy", "U Školky", "U Teplárny", "U Václava", "Univerzita", "Úřad Lochotín", "Ústřední hřbitov", "V Ráji", "V Zahradách", "Valcha", "Vejprnice, bytovky", "Vejprnice, Náves", "Vejprnice, Pod farou", "Věznice Bory", "Vinice", "Višňovka", "Vltava", "Vodárna", "Vochov", "Vochov, rozc.", "Vozovna Slovany", "Vřesová", "Waltrova", "Zadní Roudná", "Zadní Skvrňany", "Zámecké náměstí", "Západočeská univerzita", "Zátiší", "Zbůch", "Zbůch, Starý důl rozc.", "Zelenohorská", "Zimní stadion", "Zoologická zahrada", "Zruč - Senec", "Zruč - Senec, rozc.", "Zruč - Senec, u Drudíků", "Zruč - Senec, U pomníku", "Zruč - Senec, V koutě", "Železniční poliklinika", "Žlutická"]
linky = {"1", "2", "4", "10", "11", "12", "13", "14", "15", "16", "17", "18", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "50", "51", "56", "58"}
transfer = "U Práce"

class ExampleDialog(Dialog):
    def print_sip_call_info(self, **call_info):
        pprint(call_info)
        
    def mapping(self, tags):
        self.logger.debug("tags mapping")
        self.logger.debug(tags)
        return tags


    async def start_session(self):
        self.sc.on("sip_call_info", self.print_sip_call_info)

    async def main(self):
        await self.slu()
        #await self.recog()
        #await self.synth()

    async def recog(self):
        gramatika =(self.grammar_from_dict("command", {"konec dialogu": {"konec", "skonči", "ukončit"},
                                                 "předvést nápovědu": "nápověda"}) + 
              self.grammar_from_dict("numbers", {1: "jedna",
                                                 #2: "dva | dvÄ›",
                                                 2: {"dva", "dvě"},
                                                 3: "tři",
                                                 4: "čtyři",
                                                 5: "pět",
                                                 6: "šest",
                                                 7: "sedm",
                                                 8: "osm",
                                                 9: "devět"})
        )
              

        pprint(gramatika)
        await self.define_slu_grammars(gramatika)
    
        while True:
            #Úvodní syntéza informuje o odjezdu nejbližšího spoje a vybídne k další interakci
            await self.synthesize_and_wait(text=vozidlo+" číslo "+linka+", směr "+smer+" přijede za "+cas+" minut. "+"Hledáte spojení nebo jiný odjezd?")
            #vstup uživatele
            result = await self.recognize_and_wait_for_asr_result(timeout=5.)
            #result = await self.recognize_and_wait_for_slu_result(timeout=5.)
            print("Result: ")
            print(result)
            
            if result is None: #je-li vstup prázdný, do výsledku se uloží None, jinak se uloží celý vstup
                words = None
            else:
                words = result["word_1best"]#.split()
                print("Words: ")
                print(words)
                print("spojení: ")
            #Pokud je vstup None
            if words is None:
                await self.display("no-input")
                await self.synthesize_and_wait(text="Hledáte spojení nebo odjezd?") #Zopakování podnětu k interakci
            
            elif ("odjezd" and "odjíždí") in words: #ne" or "nezkoušel" in words) and not "ano" or "zkoušel" in words:
                if ("nejbližší" or "teď" or "nejdřív" or "první") in words:
                    await self.display(text=vozidlo+" číslo "+linka+", směr "+smer+" přijede za "+cas+" minut.")
                    await self.synthesize_and_wait(text=vozidlo+" číslo "+linka+", směr "+smer+" přijede za "+cas+" minut.")
                elif ("patnáct" and "dvacet") in words:
                    await self.display(text=vozidlo+" číslo "+linka+", směr "+smer+" přijede v 15:29")
                    await self.synthesize_and_wait(text=vozidlo+" číslo "+linka+", směr "+smer+" přijede v 15:29")
                break
            
            elif ("spojení" and "dostanu" and "jak") in words: #zkoušel" in words and not "ne" or "nezkoušel" in words:
                zastavka = najdiZastavku(words, zastavky)
                synteza = get_syntezu(get_spoje("Technická", zastavka))
                await self.display(text=synteza)
                await self.synthesize_and_wait(text=synteza)
                
                #await self.display("V patnáct dvacet nastupte do "+vozidlo+" číslo "+linka+" směr "+smer+" a vystupte na zastávce "+transfer+"."+"Tam přestupte na trolejbus číslo 16 a pokračujte do cílové zastávky.")
                #await self.synthesize_and_wait(text=f"V patnáct dvacet nastupte do "+vozidlo+" číslo "+linka+" směr "+smer+" a vystupte na zastávce "+transfer+"."+"Tam přestupte na trolejbus číslo 16 a pokračujte do cílové zastávky.")
                
                """ subresult = await self.recognize_and_wait_for_asr_result(timeout=5.)
                if subresult is None:
                    subwords = None
                else:
                    subwords = subresult["word_1best"]
                if subwords is None:
                    await self.display("no-input")
                    await self.synthesize_and_wait(text="Haló, jste tam?")
                                   
                elif "ne" in subwords:
                        await self.display("Tak to musíte zapnout. Zatím na shledanou.")
                        await self.synthesize_and_wait(text=f"Tak to musíte zapnout. Zatím na shledanou.")
                        break
                elif "ano" in subwords:
                        await self.display("Tak to je divné. S tím si asi nevím rady ani já. Zatím na shledanou.")
                        await self.synthesize_and_wait(text=f"Tak to je divné. S tím si asi nevím rady ani já. Zatím na shledanou.")
                        break
                elif "ukončit" in subwords:
                    await self.display("Tak nic. Na shledanou.")
                    await self.synthesize_and_wait(text=f"Tak nic. Na shledanou") 
                    break
                else:
                    text = f"Řekl jste {subwords}. Tomu nerozumím."
                    await self.display(text)
                    await self.synthesize_and_wait(text)  """                   
                
            elif "ukončit" in words:
                await self.display("Tak nic. Na shledanou.")
                await self.synthesize_and_wait(text=f"Tak nic. Na shledanou")
                break            
                
            else:
                text = f"Řekl jste {words}. Tomu nerozumím."
                await self.display(text)
                await self.synthesize_and_wait(text)

    async def slu(self):
        """
        GRM = [{ 'entity': 'akce', 'data': open('myGRM/akce.abnf', 'rt', encoding="utf-8").read(),'mapping':self.mapping, 'type': 'abnf-inline'},
               { 'entity': 'stops', 'data': open('myGRM/stops_gen.abnf', 'rt', encoding="utf-8").read(), 'mapping':self.mapping, 'type': 'abnf-inline'},
               { 'entity': 'cas', 'data': open('myGRM/cas.abnf', 'rt', encoding="utf-8").read(), 'mapping':self.mapping, 'type': 'abnf-inline'},
               { 'entity': 'cas_rel', 'data': open('myGRM/cas_rel.abnf', 'rt', encoding="utf-8").read(), 'mapping':self.mapping, 'type': 'abnf-inline'},
               { 'entity': 'pohyby', 'data': open('myGRM/pohyby.abnf', 'rt', encoding="utf-8").read(), 'mapping':self.mapping, 'type': 'abnf-inline'}
              ]

        
        await self.define_slu_grammars(GRM)
        """
        
        await self.use_slu_grammars({'akce':self.mapping,'stops_gen':self.mapping,'cas':self.mapping,'cas_rel':self.mapping,'pohyby':self.mapping})
        
        #self.sc.dm_recieve_message(tabule())
        
        await self.synthesize_and_wait(text="Zdravím, jsem chytrá zastávka em há dé. Chcete-li mluvit, stiskněte tlačítko.")
        
        while True:
            
            await self.sc.dm_send_message()

            result = await self.recognize_and_wait_for_slu_result(timeout=5.)
            print("Entities: ")
            print(result.entities)
            print("Entity_1best")
            print(result.entity_1best)
            print(" ")
            """print(result.zastavky)
            print(result.requests)
            print(" ")
            print(result.zastavky.keys())
            print("KONEC")"""
            """if result.all.numbers:
                cisla = ", ".join(str(num) for num in result.all.numbers)
                soucet = sum(result.all.numbers)

                prompt = f"Součet čí­sel {cisla} je {soucet}"
                await self.display(prompt)
                await self.synthesize_and_wait(prompt)

            elif result.first.command:
                command = result.first.command

                await self.display(command)
                await self.synthesize_and_wait(text=f"Rozpoznán pří­kaz {command}")"""
                
            """if result.zastavky:
                synteza = get_syntezu(get_spoje("Technická", result.zastavky.first))
                await self.display(text=synteza)
                await self.synthesize_and_wait(text=synteza)
            
            
            else:
                await self.synthesize_and_wait(text="Žádný příkaz nerozpoznán")"""
            
            cas = result.cas.first
            zastavka = result.stops_gen.first
            if result.stops_gen:
            
                if ('spojeni' in result.akce) and result.cas:
                    spoje = get_spoje("Technická", zastavka, cas)
                    aktSpoj = spoje[0]
                    synteza = get_syntezu(spoje, "spojeni_cas")
                    #text = aktSpoj[0][0]+"\nTechnická "+aktSpoj[0][1][0][1]+"\n"+aktSpoj[0][1][1][0]+" "+aktSpoj[0][1][1][1]
                    
                    text = '<style>td{width:12em}</style><div style="border-top:1px solid black; border-bottom:1px solid black;"><table><tr><td><b>'+aktSpoj[0][0]+'</b></td></tr><tr><td>Technická</td><td>'+aktSpoj[0][1][0][1]+'</td></tr><tr><td>'+aktSpoj[0][1][1][0]+'</td><td>'+aktSpoj[0][1][1][1]+'</td></tr></table>'
                                 
                    if len(aktSpoj)>1:
                        for i in range(1, len(aktSpoj)):
                            #text = text + "<br>"+aktSpoj[i][0]+"<br>"+aktSpoj[i-1][1][1][0]+" "+aktSpoj[i][1][0][1]+"<br>"+aktSpoj[i][1][1][0]+" "+aktSpoj[i][1][1][1]+"<br>"
                            
                            text = text + '<br><table><tr><td><b>'+aktSpoj[i][0]+'</b></td></tr><tr><td>'+aktSpoj[i-1][1][1][0]+'</td><td>'+aktSpoj[i][1][0][1]+'</td></tr><tr><td>'+aktSpoj[i][1][1][0]+'</td><td>'+aktSpoj[i][1][1][1]+'</td></tr></table>'
                        text = text+'</div>'
                            
                    await self.display(text=text)
                    synteza = synteza.split (". ")
                    for veta in synteza:
                        await self.synthesize_and_wait(text=veta)
                    
                    upresneni = await self.recognize_and_wait_for_slu_result(timeout=5.)
                    
                    if upresneni.cas_rel and ('+' in upresneni.pohyby):
                        print("I'm in!")
                        novy_cas = time_move (cas, upresneni.cas_rel.first, upresneni.pohyby.first)
                        print(novy_cas)
                        spoje = get_spoje("Technická", zastavka, novy_cas)
                        aktSpoj = spoje[0]
                        print(aktSpoj)
                        synteza = get_syntezu(spoje, "spojeni_cas")
                        #text = aktSpoj[0][0]+"\nTechnická "+aktSpoj[0][1][0][1]+"\n"+aktSpoj[0][1][1][0]+" "+aktSpoj[0][1][1][1]
                        text = '<style>td{width:12em}</style><div style="border-top:1px solid black; border-bottom:1px solid black;"><table><tr><td><b>'+aktSpoj[0][0]+'</b></td></tr><tr><td>Technická</td><td>'+aktSpoj[0][1][0][1]+'</td></tr><tr><td>'+aktSpoj[0][1][1][0]+'</td><td>'+aktSpoj[0][1][1][1]+'</td></tr></table>'
                        if len(aktSpoj)>1:
                            for i in range(1, len(aktSpoj)):
                                #text = text + "\n"+aktSpoj[i][0]+"\n"+aktSpoj[i-1][1][1][0]+" "+aktSpoj[i][1][0][1]+"\n"+aktSpoj[i][1][1][0]+" "+aktSpoj[i][1][1][1]
                                text = text + '<br><table><tr><td><b>'+aktSpoj[i][0]+'</b></td></tr><tr><td>'+aktSpoj[i-1][1][1][0]+'</td><td>'+aktSpoj[i][1][0][1]+'</td></tr><tr><td>'+aktSpoj[i][1][1][0]+'</td><td>'+aktSpoj[i][1][1][1]+'</td></tr></table>'
                            text = text+'</div>'
                        await self.display(text=text)
                        synteza = synteza.split (". ")
                        for veta in synteza:
                            await self.synthesize_and_wait(text=veta)
                            
                    elif upresneni.cas_rel and ('-' in upresneni.pohyby):
                        print("I'm in!")
                        novy_cas = time_move (cas, upresneni.cas_rel.first, upresneni.pohyby.first)
                        print(novy_cas)
                        spoje = get_spoje("Technická", zastavka, novy_cas)
                        aktSpoj = spoje[0]
                        print(aktSpoj)
                        synteza = get_syntezu(spoje, "spojeni_cas")
                        #text = aktSpoj[0][0]+"\nTechnická "+aktSpoj[0][1][0][1]+"\n"+aktSpoj[0][1][1][0]+" "+aktSpoj[0][1][1][1]
                        text = '<style>td{width:12em}</style><div style="border-top:1px solid black; border-bottom:1px solid black;"><table><tr><td><b>'+aktSpoj[0][0]+'</b></td></tr><tr><td>Technická</td><td>'+aktSpoj[0][1][0][1]+'</td></tr><tr><td>'+aktSpoj[0][1][1][0]+'</td><td>'+aktSpoj[0][1][1][1]+'</td></tr></table>'
                        if len(aktSpoj)>1:
                            for i in range(1, len(aktSpoj)):
                                #text = text + "\n"+aktSpoj[i][0]+"\n"+aktSpoj[i-1][1][1][0]+" "+aktSpoj[i][1][0][1]+"\n"+aktSpoj[i][1][1][0]+" "+aktSpoj[i][1][1][1]
                                text = text + '<br><table><tr><td><b>'+aktSpoj[i][0]+'</b></td></tr><tr><td>'+aktSpoj[i-1][1][1][0]+'</td><td>'+aktSpoj[i][1][0][1]+'</td></tr><tr><td>'+aktSpoj[i][1][1][0]+'</td><td>'+aktSpoj[i][1][1][1]+'</td></tr></table>'
                            text = text+'</div>'
                        await self.display(text=text)
                        synteza = synteza.split (". ")
                        for veta in synteza:
                            await self.synthesize_and_wait(text=veta)
            
                elif 'spojeni' in result.akce:
                    spoje = get_spoje("Technická", result.stops_gen.first, 0)
                    synteza = get_syntezu(spoje, "spojeni")
                    aktSpoj = spoje[0]
                    #text = aktSpoj[0][0]+"\nTechnická "+aktSpoj[0][1][0][1]+"\n"+aktSpoj[0][1][1][0]+" "+aktSpoj[0][1][1][1]
                    text = '<style>td{width:12em}</style><div style="style="border-top:1px solid black; border-bottom:1px solid black;"><table><tr><td><b>'+aktSpoj[0][0]+'</b></td></tr><tr><td>Technická</td><td>'+aktSpoj[0][1][0][1]+'</td></tr><tr><td>'+aktSpoj[0][1][1][0]+'</td><td>'+aktSpoj[0][1][1][1]+'</td></tr></table>'
                    if len(aktSpoj)>1:
                        for i in range(1, len(aktSpoj)):
                            #text = text + "\n"+aktSpoj[i][0]+"\n"+aktSpoj[i-1][1][1][0]+" "+aktSpoj[i][1][0][1]+"\n"+aktSpoj[i][1][1][0]+" "+aktSpoj[i][1][1][1]
                            text = text + '<br><table><tr><td><b>'+aktSpoj[i][0]+'</b></td></tr><tr><td>'+aktSpoj[i-1][1][1][0]+'</td><td>'+aktSpoj[i][1][0][1]+'</td></tr><tr><td>'+aktSpoj[i][1][1][0]+'</td><td>'+aktSpoj[i][1][1][1]+'</td></tr></table>'
                        text = text+'</div>'
                    await self.display(text=text)
                    await self.synthesize_and_wait(text=synteza)
                    
                    #TADY ZACINA UPRESNENI
                    upresneni = await self.recognize_and_wait_for_slu_result(timeout=5.)
                    cas = aktSpoj[0][1][0][1]
                    if upresneni.cas_rel and ('+' in upresneni.pohyby):
                        print("I'm in!")
                        novy_cas = time_move (cas, upresneni.cas_rel.first, upresneni.pohyby.first)
                        print(novy_cas)
                        spoje = get_spoje("Technická", zastavka, novy_cas)
                        aktSpoj = spoje[0]
                        print(aktSpoj)
                        synteza = get_syntezu(spoje, "spojeni_cas")
                        #text = aktSpoj[0][0]+"\nTechnická "+aktSpoj[0][1][0][1]+"\n"+aktSpoj[0][1][1][0]+" "+aktSpoj[0][1][1][1]
                        text = '<style>td{width:12em}</style><div style="style="border-top:1px solid black; border-bottom:1px solid black;"><table><tr><td><b>'+aktSpoj[0][0]+'</b></td></tr><tr><td>Technická</td><td>'+aktSpoj[0][1][0][1]+'</td></tr><tr><td>'+aktSpoj[0][1][1][0]+'</td><td>'+aktSpoj[0][1][1][1]+'</td></tr></table>'
                        if len(aktSpoj)>1:
                            for i in range(1, len(aktSpoj)):
                                #text = text + "\n"+aktSpoj[i][0]+"\n"+aktSpoj[i-1][1][1][0]+" "+aktSpoj[i][1][0][1]+"\n"+aktSpoj[i][1][1][0]+" "+aktSpoj[i][1][1][1]
                                text = text + '<br><table><tr><td><b>'+aktSpoj[i][0]+'</b></td></tr><tr><td>'+aktSpoj[i-1][1][1][0]+'</td><td>'+aktSpoj[i][1][0][1]+'</td></tr><tr><td>'+aktSpoj[i][1][1][0]+'</td><td>'+aktSpoj[i][1][1][1]+'</td></tr></table>'
                            text = text+'</div>'
                        await self.display(text=text)
                        synteza = synteza.split (". ")
                        for veta in synteza:
                            await self.synthesize_and_wait(text=veta)
                            
                    elif upresneni.cas_rel and ('-' in upresneni.pohyby):
                        print("I'm in!")
                        novy_cas = time_move (cas, upresneni.cas_rel.first, upresneni.pohyby.first)
                        print(novy_cas)
                        spoje = get_spoje("Technická", zastavka, novy_cas)
                        aktSpoj = spoje[0]
                        print(aktSpoj)
                        synteza = get_syntezu(spoje, "spojeni_cas")
                        #text = aktSpoj[0][0]+"\nTechnická "+aktSpoj[0][1][0][1]+"\n"+aktSpoj[0][1][1][0]+" "+aktSpoj[0][1][1][1]
                        text = '<style>td{width:12em}</style><div style="style="border-top:1px solid black; border-bottom:1px solid black;"><table><tr><td><b>'+aktSpoj[0][0]+'</b></td></tr><tr><td>Technická</td><td>'+aktSpoj[0][1][0][1]+'</td></tr><tr><td>'+aktSpoj[0][1][1][0]+'</td><td>'+aktSpoj[0][1][1][1]+'</td></tr></table>'
                        if len(aktSpoj)>1:
                            for i in range(1, len(aktSpoj)):
                                #text = text + "\n"+aktSpoj[i][0]+"\n"+aktSpoj[i-1][1][1][0]+" "+aktSpoj[i][1][0][1]+"\n"+aktSpoj[i][1][1][0]+" "+aktSpoj[i][1][1][1]
                                text = text + '<br><table><tr><td><b>'+aktSpoj[i][0]+'</b></td></tr><tr><td>'+aktSpoj[i-1][1][1][0]+'</td><td>'+aktSpoj[i][1][0][1]+'</td></tr><tr><td>'+aktSpoj[i][1][1][0]+'</td><td>'+aktSpoj[i][1][1][1]+'</td></tr></table>'
                            text = text+'</div>'
                        await self.display(text=text)
                        synteza = synteza.split (". ")
                        for veta in synteza:
                            await self.synthesize_and_wait(text=veta)
                    #TADY KONCI UPRESNENI
                    

                
                    
                
                
            elif ('odjezd' in result.akce) and ('now' in result.cas):
                synteza = get_syntezu(get_spoje("Technická", "Bory", 0), "odjezd_now")
                await self.display(text=synteza)
                await self.synthesize_and_wait(text=synteza)
                
            elif ('odjezd' in result.akce) and result.cas:
                synteza = get_syntezu(get_spoje("Technická", "Bory", result.cas.first), "odjezd")
                await self.display(text=synteza)
                await self.synthesize_and_wait(text=synteza)
            
            
            else:
                await self.synthesize_and_wait(text="Žádný příkaz nerozpoznán")
                
            





    async def synth(self):
        await self.synthesize_and_wait(text=f"NĂˇsleduje pĹ™ehlĂ­dka tĂ© tĂ© es hlasĹŻ.")

        factor = 0.5

        voices = {"Iva": "Iva210",
                  "Jan": "Jan210",
                  "JiĹ™Ă­": "Jiri210",
                  "KateĹ™ina": "Katerina210",
                  "Radka": "Radka210",
                  "Stanislav": "Stanislav210",
                  "Alena": "Alena210"}

        voices_keys = []
        
        gains = [1.0, 1/4, 1/8, 1/16]

        for i in range(10):
            if not voices_keys:
                voices_keys = list(voices)
            voice = random.choice(voices_keys)
            voices_keys.remove(voice)
            gain = random.choice(gains)
            await self.display(f"voice: {voice}, gain: {gain}")
            await self.synthesize_and_wait(text=f"Ahoj, jĂˇ jsem {voice}.", voice=voices[voice], gain=gain)
            await asyncio.sleep(0.2)






if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s', level=logging.DEBUG)
    #repeat_tabule()

    SpeechCloudWS.run(ExampleDialog, address="0.0.0.0", port=8894, static_path="./static")
