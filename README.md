## Analiza optymalnej lokalizacji farmy fotowoltaicznej
Projekt dotyczy wskazania optymalnej lokalizacji do wybudowania nowej farmy fotowoltaicznej dla obszaru gminy Świeradów Zdrój (województwo dolnośląskie, powiat lubański).

#### Kryteria wskazania optymalnej lokalizacji inwestycji
| Lp | Kryterium | Parametry |
| ------------- | ------------- | ------------- |
| 1  | Odległość od rzek i zbiorników wodnych | jak najbliżej (nieprzekraczalna strefa ochronna 100m)  |
| 2  | Odległość od budynków mieszkalnych | jak najdalej, powyżej 150m |
| 3  | Pokrycie terenu  | nie w lesie, powyżej 15m od lasu, optymalnie powyżej 100m  |
| 4  | Dostęp do dróg utwardzonych  | jak największe zagęszczenie |
| 5  | Nachylenie stoków | optymalnie – płasko, maksymalnie 10%  |
| 6  | Dostęp światła słonecznego  | optymalnie: stoki południowe (SW-SE) |
| 7  | dobry dojazd od istotnych drogowych węzłów komunikacyjnych | jak najkrótszy czas dojazdu |

##### Po połączeniu kryteriów i stworzeniu mapy przydatności:
| Lp | Kryterium | Parametry |
| ------------- | ------------- | ------------- |
| 1  | Ocena przydatności terenu (próg przydatności) | 80% / 90% max. przydatności |
| 2  | Przydatne działki / grupy działek | min. 60 % działki na terenie przydatnym |
| 3  | Powierzchnia i min. szerokość obszaru | 2ha / 50m |
| 4  | Koszt przyłącza do sieci SN (mapy kosztów) | jak najniższy |

#### Uruchomienie
- **analizaLokalizacjiFarmy.ipynb** - notebook możliwy do uruchomienia w środowisku ArcGiS, wykonuje analizę dla gminy Świeradów zdrój, możliwa jest zmiana parametrów w kodzie i uruchomienie dla dowolnej gminy
- **analiza_lokalizacji_farmy.pyt** - Toolbox .pyt, po zaimportowaniu go do ArcGiSa należy podać odpowiednie parametry (wymagane do analizy warstwy z BDOT10k dla dowolnej gminy):
  ![image](https://github.com/user-attachments/assets/8c783faa-b8e5-4a77-94a3-14bfab1b7810)
  
