Arbeitsjounal
###############



.. list-table::
   :widths: 10 70 10 10
   :header-rows: 1


   * - Datum
     - Bearbeitete Inhalte 
     - Stolpersteine 
     - Planung
   * - vor 23.07.2019
     -
     - 
     -
   * - 23.07.2019
     - Entwicklung von abspeichern von Programm Versionen. Ich werde alles innerhalb eines Versions-Ordner Entwickeln. Dies enthält nebst den Jupyter-Notebook auch alle Input und output Files (z.B. Midi, Audio ..). Bei Einer Versionierung wird vom .ipynb ein .rst exportiert. Die Versionsordner befinden sich unglücklicherwise im /doc Ordenr. Dies ist nötig weil man in Sphinx nur Kompliziert Dateien ausserhalb des Dokumentationsordner einbeinden kann. Auch vermeide ich die Versionsordner umherzuschieben. Ansonsten müsste ich die Verlinkungen z.B. für die Audio-Files jedes mal neu erstellen.
     
       Verschiedene Integrationen von Audios in die Sphinx-Dokumentation angeschaut. Spinx und read the docs haben keinen eigenen Audio player. Ich erwog die output Dateien auf Youtube hochzuladen und das Audio in die Dokumentation einzubinden. Glücklicherweise habe ich noch einen weg gefunden, in dem man die Dateien direckt von Github her einbettet.
       
       gr
     - 
     -






.. code:: python

    print(seq)
    notes1 = NoteSeq(seq)
    midi = Midi(1, tempo=120)
    midi.seq_notes(notes1, track=0)
    midi.write("demo.mid")


.. parsed-literal::

    C C D D F G A B B B B B A G F D D C 



