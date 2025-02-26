# IMG Upload Frontend

Das ist das Frontend für das Image Upload backend.

## Installation

Folgende Befehle führt man aus um das Frontend zu installieren

``` bash
git clone https://github.com/Aurvandill/img_upload.git
cd img_upload/frontend
npm install
```

Danach editiert man die Datei `img_upload/frontend/src/lib/defines` und aktualisiert den Parameter `API_URL` je nachdem wo die API gehostet ist. (Die API braucht SSL!)

Danach kann man die API im Debug Modus starten mit den Befehl

``` bash
npm run dev -- --host
```

## Building

To be written