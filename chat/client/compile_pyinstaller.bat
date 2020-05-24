python -m PyInstaller --noconfirm --log-level=DEBUG ^
    --debug all ^
    --onedir ^
    --paths "C:\Program Files\Python37\Lib\site-packages\PyQt5\Qt\bin" ^
    --distpath pydist ^
    --hiddenimport PyQt5.sip ^
    --hiddenimport sqlalchemy ^
    --hiddenimport sqlalchemy.orm ^
    --hiddenimport sqlalchemy.ext.declarative ^
    --hiddenimport sqlalchemy.orm ^
    --hiddenimport hmac ^
    --hiddenimport Crypto ^
    --hiddenimport Crypto.PublicKey ^
    --hiddenimport Crypto.PublicKey.RSA ^
    --exclude-module numpy ^
    --exclude-module scipy ^
    --noupx ^
    src/clientMain.py