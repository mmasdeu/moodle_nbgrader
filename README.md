# Funcionament de nbgrader i moodle_nbgrader.

Per per correcció automàtica de notebooks de Jupyter. Adaptat a la Universitat Autònoma de Barcelona (UAB).

Aquestes instruccions han estat adaptades de <https://nbgrader.readthedocs.io/en/stable/user_guide/installation.html> i de <https://github.com/johnhw/moodle_nbgrader>.

## Instal·lació (només la primera vegada)

### Instal·lació de NBGrader

Cal fer servir el gestor de paquets del sistema, per instal·lar els paquests *Python*: `nbgrader`, `pdfkit` i `fire`. Tambés es pot fer amb `conda` o `mamba`:
```
$ mamba install nbgrader
```

### Instal·lació de moodle_nbgrader

Aquests scripts ens serveixen per interactuar amb cursos del Moodle.

1. Descarreguem els scripts:

  `$ git clone https://github.com/mmasdeu/moodle_nbgrader.git ~/moodle_nbgrader`

## Creació d'una tasca

1. Anem a la carpeta on volem mantenir les diferents entregues

   ```
   $ mkdir -p ~/AlgebraLineal
   $ cd ~/AlgebraLineal
   ```

2. Creem la configuració inicial, i hi copiem el fitxer inicial de configuració, adaptat a la UAB.

   ```
   $ wget https://raw.githubusercontent.com/mmasdeu/moodle_nbgrader/master/nbgrader_config.py
   $ wget https://raw.githubusercontent.com/mmasdeu/moodle_nbgrader/master/header.ipynb -P source/
   $ jupyter lab (s'obre una finestra/pestanya al navegador)
   ```

3. Editem el fitxer `source/header.ipynb`, si volem.
4. Cliquem la pestanya *Formgrader* que ha aparegut.
5. Cliquem *+ Add new assignment...* (**No feu servir espais al nom!**)
6. Cliquem el llapis *Edit*
7. Cliquem el nom  (a la columna *Name*)

Es poden afegir nous fitxers de Sage/Python. Cal anar a *View -> Cell Toolbar -> Create Assignment*

8. Cliquem el botó per Generar la tasca: *Generate*.
9. El podem veure clicant a *Preview*.
10. Podem penjar al Moodle el fitxer resultant, que trobarem a la carpeta `releases/`.

### Avaluació de proves

Podem avaluar una tasca per veure que funciona tal i com tenim previst. Per fer-ho, simplement cal
crear un directori `~/AlgebraLineal/submitted/JohnSmith/Examen/` i posar-hi a dins el fitxer corresponent.
L'avaluació automàtica es pot fer com en el pas 7 de la secció següent.

## Correcció de la tasca amb moodle_nbgrader

1. Al Campus Virtual, cliquem a *Visualitza totes les trameses*.
2. *Acció de qualificar* -> *Descarrega totes les trameses*. Cal habilitar l'opció **Descarrega les trameses en carpetes**.
3. Als *Paràmetres de la Tasca* hem d'habilitar, dins la secció *Tipus de retroacció* les caselles **Full de qualificació fora de línia** i **Fitxers de retroalimentació**, i desabilitar les altres dues (Comentaris de retroalimentació i PDF amb comentaris).
4. També hem de baixar el full de qualificacions: *Descarrega el full de càlcul per qualificar*.
5. Copiem l'arxiu .zip i el full a `imports/`:

   ```
   $ mkdir -p ~/AlgebraLineal/imports
   $ cp tasca.zip ~/AlgebraLineal/imports/Examen.zip
   $ cp full.csv ~/AlgebraLineal/imports/Examen.csv
   ```

6. Generem els fitxers per avaluar

   `$ ~/moodle_nbgrader/moodle_nbgrader collect Examen`

7. Ara podem fer l'avaluació automàtica:

   `$ nbgrader autograde Examen`

8. Si cal, des de la interfície web fem la part manual de la correcció.
9. Si no ho hem fet des de la interfícia web, podem generar els fitxers de retroacció amb la comanda següent:

   `$ nbgrader generate_feedback Examen`
   
11. Generem el fitxer de notes i el *zip* amb la retroacció:

   ```
   $ ~/moodle_nbgrader/moodle_nbgrader gradesheet Examen
   ```

11. A la carpeta `exports/` hi trobarem els fitxers:

    - `exports/Examen.csv` -> Per pujar com *Puja un full de qualificació*.
    - `exports/Examen_feedback.zip` -> Per pujar com *Penja múltiples fitxers de retroacció en un zip*.
