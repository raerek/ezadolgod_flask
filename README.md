# Ez a dolgod! - feladatlista-alkalmazás Pythonban

Ez az alkalmazás Pythonban készült Flask keretrendszer felhasználásával, főként a konténerizációs munkafolyamat oktatására.
Egyszerű feladatlistát valósít meg. A feladatok alapesetben SQLite-adatbázisfájlba kerülnek, MySQL használatát lásd lenn.  
- [Az alkalmazás telepítése fizikai vagy virtuális gépre, és futtatása](#telepites)  
- [MySQL- vagy MariaDB-adatbázis használata](#mysql)  
- [Konténerkészítés](#kontener)  

<a name="telepites"></a>
## Az alkalmazás telepítése fizikai vagy virtuális gépre, és futtatása
A leírás Ubuntu 20.04 és 22.04 friss telepítésen tesztelve.  
A # root parancssort jelöl, a $ egyszerű felhasználóét az alábbiakban.

### Előkészületek
PIP telepítése:  
`# apt install python3-pip`

Virtuális környezet (venv) telepítése:  
`# apt install python3-venv`

A programot bárhogy a gépre másolhatjuk.  
Ha git használata mellett döntünk, akkor először a git telepítése szükséges:  
`# apt install git`  
Ezt követően klónozzuk a github-tárolót:  
`$ git clone https://github.com/raerek/ezadolgod_flask.git`

Belépünk a megfelelő mappába:  
`$ cd ezadolgod_flask`  

A virtuális környezet kialakítása:  
`$ python3 -m venv venv`  
és aktiválása:  
`$ . ./venv/bin/activate`

A szükséges modulok telepítése PIP-pel:  
`(venv)$ pip3 install -r requirements.txt`

A következő modulok és függőségeik települnek:  
- Flask  
- Flask-SQLAlchemy  
- gunicorn (ha "élesben" futtatnánk az alkalmazást)  
- PyMySQL

### Az alkalmazás futtatása
- A szerver futtatása fejlesztő/hibakereső módban az 5000-es porton. A http://localhost:5000/ címet megnyitva érhető el az alkalmazás.  
`(venv)$ python3 app.py`  
- A szerver futtatása fejlesztő/hibakereső módban az 5000-es porton. A http://<szerver-IP-címe>:5000/ címet megnyitva érhető el az alkalmazás.  
`(venv)$ flask run --host 0.0.0.0`  
- A szerver futtatása "éles" módban futtatja a 8000-es porton.  
`(venv)$ gunicorn --bind 0.0.0.0:8000 --workers 3 app:app`  

## Az alkalmazás elkészítéséhez felhasznált források
Lásd a `credits.txt` fájlt.

<a name="mysql"></a>
## MySQL- vagy MariaDB-adatbázis használata
A megfelelő adatbázis kialakítása és a kapcsolati felhasználó létrehozása a MySQL-szerverhez kapcsolódva:  
`CREATE DATABASE ezadolgod;`  
`CREATE TABLE ezadolgod.todo (id INT PRIMARY KEY AUTO_INCREMENT, content VARCHAR(200) NOT NULL, date_created DATETIME);`  
`GRANT ALL PRIVILEGES ON ezadolgod.* TO 'ezadolgoduser'@'%' IDENTIFIED BY 'EzEgyJelszo321';`  

Az adatbázist MYSQL_URI környezeti változó értékeként kell megadni. Ha az alkalmazás talál ilyen környezeti változót, akkor az itt megadott adatbázishoz fordul, ha nem, akkor az alapértelmezett SQLite-adatbázist használja.  
A fenti utasításokkal létrehozott adatbázis használatához a  
`ezadolgoduser:EzEgyJelszo321@<szerver-címe-vagy-neve>/ezadolgod`  
URI-t kell megadni.  
Ha portot is megadnánk, akkor:  
`ezadolgoduser:EzEgyJelszo321@<szerver-címe-vagy-neve>:3306/ezadolgod`  
Néhány szerveren (pl. az Azure-ban futó MySQL-szerveren) a felhasználónevet az adatbázisszerver nevével együtt kell megadnunk:  
`ezadolgoduser@teszt01:EzEgyJelszo321@teszt01.mysql.database.azure.com:3306/ezadolgod`  

SSL-kapcsolat használata a MySQL-szerverhez való kapcsolódáskor:  
A kapcsolathoz szükség van az adatbázishoz tartozó tanúsítványhitelesítő tanúsítványára, azaz a CA-cert fájlra (pem formátumban). Két módon adhatjuk meg a fájlt az alkalmazásunknak:
- A fájlt bemásolhatjuk a `certs` mappába, ilyenkor `CACERT_FILE` nevű környezeti változóban kell megadnunk a fájl nevét (a mappáét nem).
- Megadhatjuk a fájl URL-jét a `CACERT_URL` nevű környezeti változóban, ilyenkor az alkalmazásunk induláskor letölti a fájlt.
A mostani verzióban hibás fájlnév vagy URL esetén az alkalmazásunk nem indul el helyesen.  

Ha bármelyik módon megadunk tanúsítványt, az alkalmazás annak használatával próbál kapcsolódni az adatbázishoz. Ha mindkét változó létezik, érdemes lehet tudni, hogy az URL magasabb precedenciájú a fájlnál.

Azure Database for MySQL esetén a megfelelő cacert-fájl [innen](https://docs.microsoft.com/en-us/azure/mysql/howto-configure-ssl) tölthető le.  
Az AWS RDS megfelelő tanúsítványai [innen](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html) tölthetők le.

<a name="kontener"></a>
## Konténerkészítés
A leírás Debian 11, Ubuntu 20.04 és 22.04 friss telepítésen biztosan működik.  
A # root parancssort jelöl, a $ egyszerű felhasználóét az alábbiakban.

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
`$ . ./venv/bin/activate`  
`(venv)$ pip install -r requirements.txt`  
`(venv)$ gunicorn --bind 0.0.0.0:8000 --workers 3 app:app`  
A szerver bármelyik IP-címének 8000-es portján elérhető az alkalmazás.  
Állítsuk meg a futását (Ctrl+C).  
Deaktiváljuk a virtuális környezetet:  
`(venv)$ deactivate`

### Docker telepítése és használatba vétele
Telepítés:  
`# apt install docker.io`

A nem-privilegizált felhasználó lehetőséget kap a Docker használatára:  
`# adduser raerek docker`  
A felhasználónak újra be kell jelentkeznie a csoporttagság-változás érvényre jutásához.

### Docker image előállítása
`$ cd ~/ezadolgod_flask`  
(Elhagyható: a Dockerfile megnyitása után a két ENTRYPOINT közül válasszuk azt, amelyik nekünk jobban megfelel. Állítsuk be a használni kívánt portot. Ha nem változtatunk, az alkalmazás a szabványos kimenetre naplózza az érkező kéréseket, és a 80-as porton érhető el.)  
`$ docker build . -t ezadolgod_flask`  

### Docker konténer futtatása és megállítása
- SQLite-adatbázisban tároljuk a feladatokat. A webszerver minden IP-címén elérhető az alkalmazás a 80-as porton.  
`$ docker container run --detach --rm --publish 80:80 --name melovan ezadolgod_flask`  
- MySQL-adatbázisban tároljuk a feladatokat. A webszerver minden IP-címén elérhető az alkalmazás a 80-as porton.  
`$ docker container run --detach --rm --publish 80:80 --env MYSQL_URI=<a fenti,  "MySQL- vagy MariaDB-adatbázis használata" részen bemutatott alakú URI> --name melovan ezadolgod_flask`  
- MySQL-adatbázisban tároljuk a feladatokat. Az adatbázisszerverhez SSL-lel kapcsolódunk, a tanúsítványhitelesítő tanúsítványát (a CACERT-fájlt) induláskor töltjük le. A webszerver minden IP-címén elérhető az alkalmazás a 80-as porton.  
`docker container run --detach --rm --publish 80:80 --env MYSQL_URI=<a fenti,  "MySQL- vagy MariaDB-adatbázis használata" részen bemutatott alakú URI> --env CACERT_URL=http(s)://<szerver>/<cacert-fájl.pem> --name melovan ezadolgod_flask`
- A konténer megállítása  
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
Szükség esetén megadhatjuk a MySQL/MariaDB használatához kellő környezeti változókat.
