# Ez a dolgod! - feladatlista-alkalmazás Pythonban

Ez az alkalmazás Pythonban készült Flask keretrendszer felhasználásával, főként a konténerizációs munkafolyamat oktatására.
Egyszerű feladatlistát valósít meg. A feladatok ebben a verzióban SQLite-adatbázisfájlba kerülnek.

## Telepítés
A leírás Ubuntu 20.04 friss telepítésen készült.

### Előkészületek
PIP telepítése:  
`apt install python3-pip`

Virtuális környezet (venv) telepítése:  
`apt install python3-venv`

A virtuális környezet kialakítása:  
`python3 -m venv venv`  
és aktiválása:  
`. ./venv/bin/activate`

A szükséges modulok telepítése PIP-pel:  
`pip3 install -r requirements.txt`

A következő modulok és függőségeik települnek:  
- Flask  
- Flask-SQLAlchemy  
- gunicorn (ha "élesben" futtatnád az alkalmazást)  

### A szerver futtatása
- `python3 app.py`  
a szervert fejlesztő/hibakereső módban futtatja az 5000-es porton. A http://localhost:5000/ címet megnyitva érhető el az alkalmazás.  
- `gunicorn --bind 0.0.0.0:8000 --workers 3 app:app`  
a szervert "éles" módban futtatja a 8000-es porton.

## Felhasznált források
Lásd a credits.txt fájlt.

## Konténerkészítés
A leírás Debian 11 friss telepítésen készült. A # root parancssort jelöl, a $ egyszerű felhasználóét az alábbiakban.

### A program beszerzése
A programot bárhogy a gépre másolhatjuk.  
Ha git használata mellett döntünk, akkor először a git telepítése szükséges:  
`# apt install git`  
Ezt követően klónozzuk a github-tárolót:  
`$ git clone https://github.com/raerek/ezadolgod_flask.git`

### A szükséges modulok telepítése és a telepítés sikerének ellenőrzése:
`# apt install python3-pip python3-venv`  
és  
`$ cd ezadolgod_flask`  
`$ python3 -m venv venv`  
`$. ./venv/bin/activate`  
`(venv)$ pip install -r requirements.txt`  
`(venv)$ gunicorn --bind 0.0.0.0:8000 --workers 3 app:app`  
A szerver bármelyik IP-címének 8000-es portján elérhető az alkalmazás.  
Állítsuk meg a futását (Ctrl+C).

### Docker telepítése és használatba vétele
Telepítés:  
`# apt install docker.io`

A nem-privilegizált felhasználó lehetőséget kap a Docker használatára (a felhasználónak újra be kell jelentkeznie a csoporttagság évényre jutásához):  
`# adduser raerek docker`

### Docker image előállítása
`$ cd ~/ezadolgod_flask`  
(Elhagyható: a Dockerfile megnyitása után a két ENTRYPOINT közül válasszuk azt, amelyik nekünk jobban megfelel. Állítsuk be a használni kívánt portot. Ha nem változtatunk, az alkalmazás a szabványos kimenetre naplózza az érkező kéréseket, és a 80-as porton érhető el.)  
`$ docker build . -t raerek/ezadolgod_flask`  

### Docker konténer futtatása és megállítása
`$ docker container run --detach --rm --publish 80:80 --name melovan ezadolgod_flask`  
A szerver minden IP-címén elérhető az alkalmazás a 80-as porton.  
`$ docker container stop melovan`

### Docker konténer közzététele dockerhubra:
`$ docker tag ezadolgod_flask raerek/ezadolgod_flask:latest`  
`$ docker login`  
`$ docker push raerek/ezadolgod_flask:latest`

### Docker konténer tesztelése:
Ha a tesztelést az image elkészítéséhez használt gépen végezzük, akkor távolítsuk el az image helyi verzióját:  
`$ docker image rm raerek/ezadolgod_flask:latest`  
Indíthatjuk a konténert:  
`$ docker container run --detach --rm --publish 80:80 --name melovan raerek/ezadolgod_flask`  



