# Funcionament de nbgrader i moodle_nbgrader.

Per per correcció automàtica de notebooks de Jupyter. Adaptat a la Universitat Autònoma de Barcelona (UAB).

Aquestes instruccions han estat adaptades de <https://nbgrader.readthedocs.io/en/stable/user_guide/installation.html> i de <https://github.com/johnhw/moodle_nbgrader>.

## Instal·lació (només la primera vegada)

### Instal·lació de NBGrader

  ```
  $ sage -pip install --user nbgrader
  $ sage -jupyter nbextension install --user --py nbgrader --overwrite
  $ sage -jupyter nbextension enable --user --py nbgrader
  $ sage -jupyter serverextension enable --user --py nbgrader
  ```

**Nota:** si es vol, es pot desinstalar l'extensió que ho fa tot més automàtic (que jo no faig servir):

  1. Desactivem *Assignment List*

  ```
  $ sage -jupyter nbextension disable --user assignment_list/main --section=tree
  $ sage -jupyter serverextension disable --user nbgrader.server_extensions.assignment_list
  ```

  2. Desactivem *Course List*

  ```
  $ sage -jupyter nbextension disable --user course_list/main --section=tree
  $ sage -jupyter serverextension disable --user nbgrader.server_extensions.course_list
  ```

### Instal·lació de moodle_nbgrader

Aquests scripts ens serveixen per interactuar amb cursos del Moodle.

1. Descarreguem els scripts:

  `$ git clone https://github.com/mmasdeu/moodle_nbgrader.git ~/moodle_nbgrader`

## Creació d'una tasca

1. Anem a la carpeta on volem mantenir les diferents entregues, i hi copiem el fitxer inicial de configuració, adaptat a la UAB.

   ```
   $ mkdir -p ~/AlgebraLineal
   $ cd ~/AlgebraLineal
   $ wget https://raw.githubusercontent.com/mmasdeu/moodle_nbgrader/master/nbgrader_configy.py
   $ wget https://raw.githubusercontent.com/mmasdeu/moodle_nbgrader/master/header.ipynb -P source/
   ```

2. Creem la configuració inicial

   ```
   $ ~/.local/bin/nbgrader generate_config
   $ sage -n jupyter` (s'obre una finestra/pestanya al navegador)
   ```
   
3. Editem el fitxer `source/header.ipynb`, si volem.
4. Cliquem la pestanya *Formgrader* que ha aparegut.
5. Cliquem *+ Add new assignment...* (**No feu servir espais al nom!**)
6. Cliquem el llapis *Edit*
7. Cliquem el nom  (a la columna *Name*)

Es poden afegir nous fitxers de sage. Cal anar a *View -> Cell Toolbar -> Create Assignment*

8. Cliquem el botó per Generar la tasca: *Generate*.
9. El podem veure clicant a *Preview*.
10. Podem penjar al Moodle el fitxer resultant, que trobarem a la carpeta `releases/`.

## Correcció de la tasca amb moodle_nbgrader

1. Al Campus Virtual, cliquem a *Visualitza totes les trameses*.
2. *Acció de qualificar* -> *Descarrega totes les trameses*.
3. També hem de baixar el full de qualificacions: *Descarrega el full de càlcul per qualificar*.
4. Copiem l'arxiu .zip i el full a `imports/`:

   ```
   $ cp tasca.zip ~/AlgebraLineal/imports/Examen.zip
   $ cp full.csv ~/AlgebraLineal/imports/Examen.csv
   ```
   
5. Generem els fitxers per evaluar (suposem que el worksheet es diu `Worksheet1.ipynb`)

   `$ python ~/moodle_nbgrader/collect_files.py Examen Worksheet1`

6. Ara podem fer l'avaluació automàtica:

   `$ ~/.local/bin/nbgrader autograde Examen`

7. Si cal, des de la interfície web fem la part manual de la correcció.
8. Generem el fitxer de notes i el de retroacció:

   `$ python ~/moodle_nbgrader/update_gradesheet.py Examen`

9. A la carpeta `exports/` hi trobarem els fitxers:

    - `exports/Examen.csv` -> Per pujar com *Puja un full de qualificació*.
    - `exports/Examen_feedback.zip` -> Per pujar com *Penja múltiples fitxers de retroacció en un zip*.
