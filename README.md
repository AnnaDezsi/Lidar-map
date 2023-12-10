# Lidar-map
Importă modulele necesare pentru a lucra cu ROS, numpy, cv2 și mesajele de tip Image, LaserScan, OccupancyGrid și MapMetaData.
Definește niște constante pentru a configura parametrii hărții, ai lidarului și ai camerei de adâncime. De exemplu, dimensiunea hărții în metri, rezoluția hărții în metri pe pixel, originea hărții în metri, raza maximă a lidarului în metri, unghiul minim și maxim al lidarului în radiani, incrementul de unghi al lidarului în radiani, raza maximă a camerei de adâncime în metri, câmpul vizual al camerei de adâncime în radiani, incrementul de unghi al camerei de adâncime în radiani, valorile pentru celulele ocupate, libere și necunoscute în harta de ocupare.
Creează un nod ROS și inițializează-l cu un nume, de exemplu ‘transbot_mapping’.
Creează un obiect bridge pentru a converti imaginile ROS în imagini OpenCV.
Creează un obiect map pentru a stoca grila de ocupare. Setează frame_id-ul, rezoluția, lățimea, înălțimea, originea și datele hărții. Inițializează datele hărții cu valoarea pentru celulele necunoscute.
Creează un publisher pentru a publica harta pe un topic, de exemplu ‘map’.
Definește o funcție callback pentru a procesa datele de scanare lidar. În această funcție, fă următoarele:
Obține poziția și orientarea robotului din header-ul scanării.
Convertește poziția robotului din metri în pixeli.
Parcurge razele scanării și obține raza și unghiul fiecărei măsurători.
Verifică dacă raza este validă, adică între raza minimă și maximă a lidarului.
Convertește raza și unghiul în frame-ul hărții, adică adaugă poziția și orientarea robotului.
Convertește coordonatele din metri în pixeli.
Verifică dacă pixelii sunt în limitele hărții.
Marchează celula corespunzătoare ca ocupată în datele hărții.
Desenează o linie de la robot la celula ocupată și marchează celulele de pe linie ca libere în datele hărții.
Definește o funcție callback pentru a procesa datele de imagine de adâncime. În această funcție, fă următoarele:
Obține poziția și orientarea robotului din header-ul imaginii.
Convertește poziția robotului din metri în pixeli.
Convertește imaginea ROS în imagine OpenCV.
Parcurge pixelii imaginii și obține valoarea de adâncime a fiecărui pixel.
Verifică dacă adâncimea este validă, adică între 0 și raza maximă a camerei de adâncime.
Convertește coordonatele pixelului în frame-ul camerei, adică folosește formula de proiecție inversă cu câmpul vizual al camerei.
Convertește frame-ul camerei în frame-ul robotului, adică rotește și translează coordonatele.
Convertește frame-ul robotului în frame-ul hărții, adică adaugă poziția și orientarea robotului.
Convertește coordonatele din metri în pixeli.
Verifică dacă pixelii sunt în limitele hărții.
Marchează celula corespunzătoare ca ocupată în datele hărții.
Desenează o linie de la robot la celula ocupată și marchează celulele de pe linie ca libere în datele hărții.
Creează un subscriber pentru a subscrie la topicul de scanare lidar, de exemplu ‘scan’, și folosește funcția callback definită anterior.
Creează un subscriber pentru a subscrie la topicul de imagine de adâncime, de exemplu ‘image’, și folosește funcția callback definită anterior.
Definește o funcție loop pentru a publica harta la o rată fixă, de exemplu 10 Hz. În această funcție, fă următoarele:
Creează un obiect rate pentru a controla frecvența buclei.
Repetă până când nodul este oprit:
Actualizează header-ul hărții cu timpul curent.
Publică harta pe topicul ales.
Așteaptă până la următoarea iterație.
Apelează funcția loop.
