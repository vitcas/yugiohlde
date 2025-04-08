pyinstaller --onefile --windowed ^
    --name=ygolde ^
    --icon=icon.ico ^
    --add-data="new_deck.py;." ^
    --add-data="settings.py;." ^
    --add-data="adv_search.py;." ^
    --add-data="slave.py;." ^
    --add-data="config.py;." ^
    --version-file=toolkit\version.txt ^
    main.py