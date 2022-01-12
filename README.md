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
`python3 app.py` a szervert fejlesztő/hibakereső módban futtatja az 5000-es porton. A http://localhost:5000/ címet megnyitva érhető el az alkalmazás.  
`gunicorn --bind 0.0.0.0:8000 --workers 3 app:app` a szervert "éles" módban futtatja a 8000-es porton.

## Felhasznált források
Lásd a credits.txt fájlt.