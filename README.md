# Krisenka Finley · web oficial

Web de una sola página: **de día** se pasea por la ilustración animada de Zaragoza y, al bajar, **anochece** y se entra en un concierto 3D que late con «Back Again».

## Qué hay
- **Entrada** sobre la propia ilustración: solo sus animaciones y dos nubes, «Entrar con sonido» y «Entrar sin sonido» (los navegadores solo dejan sonar música tras un clic). Al entrar aparecen las nubes del menú y las zonas interactivas.
- **Portada de día**, por capas: el fondo (WebGL: el río fluye hacia el puente, las nubes respiran y el sol proyecta rayos) y encima la cantante, que se balancea; el nombre, que respira y se aviva al pasar por encima; los ramos de flores, que se mecen y se inclinan con las ráfagas de viento; y el siluro, que salta y se sumerge. Las nubes del menú son botones, la guitarra suena y el sol gira. En pantallas verticales el nombre va aparte, arriba, para que se lea entero.
- **Atardecer**: al bajar, la ilustración se oscurece y aparece el túnel de neón 3D (Three.js) que avanza con el scroll.
- **Viaje por el túnel**: cada sección es un disco que sale del fondo girando, se para para leerlo y sale volando. Los vinilos de Música salen uno a uno del centro.
- **Música**: reproductor de «Back Again» con ecualizador real, vinilos que giran y, al pulsar uno, su **caja de CD se abre** y muestra el disco.
- **Recorrido automático**: empieza solo al entrar y se para en cuanto el visitante toca la rueda, la pantalla o el teclado.
- **Reproductor flotante** con el progreso de la canción.
- **Ligera**: la canción solo se descarga al escucharla y el 3D se descarga y se prepara durante la entrada (así no da tirones al aparecer), las imágenes van en WebP y, si el equipo va justo, la portada y el túnel bajan su resolución solos. Solo el ecualizador sigue a la música; el resto de animaciones van solas.
- Con «reducir movimiento» activado, todo se muestra estático.

## Editar contenido
Todo se cambia en **`js/data.js`**, explicado con ejemplos. Se edita desde GitHub con el lápiz («Edit this file») y «Commit changes».

- **Canción principal** (la que suena al entrar): `cancionPrincipal`.
- **Plataformas** (Spotify, Apple Music, YouTube, Bandcamp, Amazon Music, Deezer): `plataformas`. Sustituye las búsquedas por la página de la artista en cada una.
- **Discos**: `discos`, con año, sello, portada y canciones `{ titulo, duracion, archivo }`. Se muestran del más nuevo al más antiguo. Para canciones sueltas, crea un «Recopilatorio» por año (hay un ejemplo en el archivo). Si un disco no tiene portada, la web le dibuja una.
- **MP3**: en la carpeta `musica/` («Add file» → «Upload files»). Siempre dentro de la web.
- **Portadas**: `assets/portadas/`, JPG cuadrado de unos 600×600.
- **Conciertos** y **otros enlaces**: `conciertos` y `enlaces`.

## Probar en local
Los efectos necesitan servirse por HTTP:

```
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Imágenes de la portada
Cada pieza es un archivo de `assets/` y su posición está en `index.html` (`data-rect="x,y,ancho,alto"`, en píxeles de la ilustración de 2000×1116):

- `portada-fondo.webp`: el paisaje sin personajes (es lo que anima el WebGL). `fx-mask.png` marca en verde el río y en azul las nubes que se mueven.
- `portada-cantante.webp`, `nombre-krisenka-finley.webp` y `portada-flor-*.webp`: con fondo transparente.
- `siluro.webp`: el pez, girado como sale del agua (su centro está en `PIVOT`, en `js/hero.js`).

Para recortar un dibujo nuevo de su fondo de papel: `python3 tools/recortar.py dibujo.jpg recorte.png`.
