# MyWallet-to-Fireflyiii
Python [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) processor for exporting [MyWallet expense manager](https://play.google.com/store/apps/details?id=com.apps.balli.mywallet) Android app database to [Firefly iii](https://github.com/firefly-iii/firefly-iii)

# What is the problem?
Althoug [MyWallet expense manager](https://play.google.com/store/apps/details?id=com.apps.balli.mywallet) is a great budget application, it lacks of advanced statistics and dashboarding, and it is for Android ecosystem only. Also, the syncronization of the data from the app has no cloud compatibility anymore. This forces to a manual creation of raw data backups. Furthermore, this app have no updates since Aug 2016.

Then, [Firefly iii](https://github.com/firefly-iii/firefly-iii) (ffiii) app came to save me: ```"Firefly III" is a (self-hosted) manager for your personal finances. It can help you keep track of your expenses and income, so you can spend less and save more```. The purpose of this project is to ETL data from MyWallet to Firefly iii.

### Dependencies

See *requirements.txt*. You can install through line:
`pip install -r /path/to/requirements.txt`

>pandas==1.3.5

# Step by step process

## 1. Exporting the MyWallet database
First, you need to export database:
1. From the main screen of the app click at "More" on the botton right
2. Go to "Backup and restore"
3. Make a new backup by clicking at "Save Backup"
 A MySQL database file will be saved at SDCard:/MyWallet/Backups in the name of XX_XX_XXXX_ExpensoDB (where XX_XX_XXXX is the current date)
4. Copy that file in anyplace of your pc

## 2. Transforming database into CSV
Once you have your database we must make it compatible with firefly-iii. To doing so, we will use the python script of this repository named ```AccounterExporter.py```
1. Edit the constant ```DB_PATH``` with full filename path to the exported MySQL database
2. (optional) Edit the constant ```OUTPUT_NAME``` with full filename path to the csv file that will be exported. Otherwise it will be saved as ```./dbexported.csv```

## 3. Load the exported database into Firefly iii
Once data has been made compatible with Firefly iii you can load it into your Firefly iii instance. To doing so you need:
1. A running [Firefly iii](https://github.com/firefly-iii/firefly-iii) (ffiii) instance
2. A running [Firefly iii Data Importer](https://github.com/firefly-iii/data-importer) (FIYI) instance, already connected with your ffiii app.

So in order to import the data, you have to go to your FIYI instance and:
1. Click on ```Import file```
2. At ```Importable file``` select the csv we previously exported
3. At ```Optional configuration file``` select the file ```FIYIcfg\mywallet.json``` wich is part of the current repository
4. Follow the import steps
5 ...
6 Profit!

# And now what?
Once its done you will have all your data imported at ffiii. There is even some [Android/ios apps](https://docs.firefly-iii.org/firefly-iii/other-pages/3rdparty/#mobile-applications) which can connect with your ffiii instance that can substitude MyWallet with ease.

I do recommend to check [ffiii documentation](https://docs.firefly-iii.org/), wich is quite good and clear.

Its worth to notice that I have included a function into the code called ```get_account_wtransfers()```, which can be handy if you want to play arround with your data from MyWallet, due to it allows you to load a single account with all of its assets (including the ones that came from transferences between accounts)
