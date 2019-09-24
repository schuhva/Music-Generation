Arbeitsjournal
###############



.. list-table::
   :widths: 10 70 10
   :header-rows: 1


   * - Datum
     - Bearbeitete Inhalte 
     - Offene Probleme
   * - vor 23.06.2019
     -
     -
   * - 23.06.2019
     - 1. Abspeicherung/Archivierung von Programm Versionen:

       Ich werde alles innerhalb eines Versions-Ordner Entwickeln. Dieser enthält nebst den Jupyter-Notebook auch alle Input und Output Files (z.B. Midi, Audio ..). Bei einer Versionierung wird vom .ipynb ein .rst exportiert. Leider muss nach dem Export mitteles Suchen und Ersetzten die Kenzeichnug der Code-Blocks von "ipython3" nach "python3" geändert wereden. Read the Docks kennt ipython nicht.

       Die Versionsordner befinden sich unglücklicherwise im /doc/realese Ordner. Dies ist nötig weil man in Sphinx nur kompliziert Dateien ausserhalb des Dokumentationsordner einbeinden kann. Die Versionsordner werden nicht in ein "Archiv" verschoben, ansonsten müssten die Verlinkungen z.B. für die Audio-Files jedes mal neu erstellen werden.

       2. Integration der Audio-Dateien in die Sphix-Dokumentation.

       Sphinx und Read the Docs haben keinen eigenen Audio player. Ich erwog die OutputDateien auf Youtube hochzuladen und das Audio auf diese Weise in die Dokumentation einzubetten. Glücklicherweise habe ich noch einen weg gefunden in dem man die Dateien direkt von Github her einbettet.

     -
   * - 30.06.2019
     - Audioplayer für midi-Files in python. 
	  
       * midi2audio funktioniert die play funktion nur über den jack Audio-Treiber. Es muss nach jedem start den FluidSyth output mit den Lautsperchern verbunden werden.
       * pygame barchete ich nicht zum laufen
       * Ich konnte den Befehl für FuidSynth im sourcecode von midi2audio so abändern, dass nun Pulseaudio verwendet wird. Es könnte auch FluidSynth "manuell" von Jupyther aus zu verwenden. 
	     
     - Unschöne Lösung um midi datein abspeilen zu lassen.
	   
       Muss manuel geändert werden.
	     
       Bei Update wieder weg.
	
   * - 21.07.2019
     - 1. Version 1.04 (Start und Basics) 
     
       * midi2audio mit musescore und VLC erstzt. Musescore bietet aus meiner Sicht die beste Soundqualität. Ein png export ist ab jetzt auch möglich.
       * Es hat drei Bespiele um die zwei verschieden Notation von Pyknon zu erklären.
       
       2. Version 1.05 Instrumente
       
       Jedem Track kan nun ein Instrument aus dem General-Midi zu geordnet weren. Mehrstimmikeit welche im tune_D Dur-Akkorde bilden und in tune_E diatonische.
       
     - Als nächstes: Ton-Längen definiren. 
     
   * - 30.07.2019
     - Version 1.06
     
       * tune_g is very similar to tune_e. It was extended such that the Volume and the note length can be defined for each note. 
       * tune_h is is still based on a scale. But on each note e specific Ornament is played. 
       
       Verion 2.01: EInführung von ersten Zufällen
       
       * Zu erst wird mit gesteuertem Zufall bestimmt ob eine note durch eine Pause ersetzt wird. Gesteuert dadurch weil nicht eine 50/50 Chanse besteht, sondern eine indivduell einstellbare. im Bsp. tune_I werden die Noten längen ebenfalls duch gesteurtem Zufall bestimmt. 
       
     -
     
     
   * - 24.08.2019
     - Version 2.02 tune_K
     
       Erstellung von komplett zufälliger Melodie in einem Berich von etwas mehr als zwei Oktaven. 
     -
     
   * - 26.08.2019
     - Version 2.03 tune_L
     
       Einführung der Melodie-Bildung nach Interwallen und nicht asoluten Noten. So werden grosse Sprünge vermieden welche seltener in Der Musik vor kommen. Stufengänge kommen häufig vor da die Warscheidlichkeit einer Sekunde im Vergleich zu anderen Interwallen grösser ist.
       
       Version 2.03 tune_M
       
       In Entwicklung: Melodie-Bildung nach Intervallen in eine Funktion überführen. Zwei Stimmig. Erweiterte Intervalle.
     -
     
   * - bis 17.09.2019
     - Version 2.03 tune_O
     
       Automatische Skalen- und Akkordgenerirung für den ganzen Midi-Range.
       
       Anpaasungen an der soundfont. Vervende nun "Compifont" und nicht mehr die Musecore Font.
     -
     
   * -
     -
     -









