Arbeitsjounal
###############



.. list-table::
   :widths: 10 70 10
   :header-rows: 1


   * - Datum
     - Bearbeitete Inhalte 
     - Offene Probleme
   * - vor 23.07.2019
     -
     -
   * - 23.07.2019
     - 1. Abspeicherung/Archivierung von Programm Versionen:
     
       Ich werde alles innerhalb eines Versions-Ordner Entwickeln. Dieser enthält nebst den Jupyter-Notebook auch alle Input und Output Files (z.B. Midi, Audio ..). Bei einer Versionierung wird vom .ipynb ein .rst exportiert. Leider muss nach dem Export mitteles Suchen und Ersetzten die Kenzeichnug der Code-Blocks von "ipython3" nach "python3" geändert wereden. Read the Docks kennt ipython nicht.
       
       Die Versionsordner befinden sich unglücklicherwise im /doc/realese Ordner. Dies ist nötig weil man in Sphinx nur kompliziert Dateien ausserhalb des Dokumentationsordner einbeinden kann. Die Versionsordner werden nicht in ein "Archiv" verschoben, ansonsten müssten die Verlinkungen z.B. für die Audio-Files jedes mal neu erstellen werden.
     
       2. Integration der Audio-Dateien in die Sphix-Dokumentation.
       
       Sphinx und Read the Docs haben keinen eigenen Audio player. Ich erwog die OutputDateien auf Youtube hochzuladen und das Audio auf diese Weise in die Dokumentation einzubetten. Glücklicherweise habe ich noch einen weg gefunden in dem man die Dateien direkt von Github her einbettet.

     -








