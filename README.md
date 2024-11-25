# MyWallet-to-Fireflyiii
Python [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) processor for exporting the [MyWallet expense manager](https://play.google.com/store/apps/details?id=com.apps.balli.mywallet) Android app database to [Firefly iii](https://github.com/firefly-iii/firefly-iii).

## The Problem
Although the [MyWallet expense manager](https://play.google.com/store/apps/details?id=com.apps.balli.mywallet) is a great budgeting application, it lacks advanced statistics and dashboards, and is limited to the Android ecosystem. Moreover, data synchronization from the app no longer supports cloud compatibility, necessitating manual backups of raw data. Additionally, the app hasn't received updates since August 2016.

Enter [Firefly iii](https://github.com/firefly-iii/firefly-iii) (ffiii), a self-hosted personal finance manager that helps track expenses and income, enabling better financial decisions. The goal of this project is to seamlessly transfer data from MyWallet to Firefly iii using an ETL process.

## Dependencies

See *requirements.txt*. You can install them with:
```sh
pip install -r /path/to/requirements.txt
```

> pandas==1.3.5

## Step-by-Step Process

### 1. Exporting the MyWallet Database
First, you need to export the database:
1. From the main screen of the app, click on "More" in the bottom right corner.
2. Go to "Backup and restore".
3. Create a new backup by clicking on "Save Backup". A MySQL database file will be saved at `SDCard:/MyWallet/Backups` with the name `XX_XX_XXXX_ExpensoDB` (where `XX_XX_XXXX` is the current date).
4. Copy this file to your computer.

### 2. Transforming the Database into CSV
Next, you need to make the database compatible with Firefly iii. Use the Python script `AccounterExporter.py` in this repository:
1. Edit the constant `DB_PATH` with the full path to the exported MySQL database.
2. (Optional) Edit the constant `OUTPUT_NAME` with the full path to the CSV file to be exported. If not specified, it will be saved as `./dbexported.csv`.

### 3. Load the Exported Database into Firefly iii
Now, load the transformed data into your Firefly iii instance. You will need:

1. A running [Firefly iii](https://github.com/firefly-iii/firefly-iii) (ffiii) instance.
2. A running [Firefly iii Data Importer](https://github.com/firefly-iii/data-importer) (FIYI) instance, connected to your ffiii app.

Before loading the data, follow these steps in Firefly iii:

1. **Create a New Account**:
   - Go to **Accounts** -> **Active accounts**.
   - Create all accounts you have in your MyWallet app.

2. **Set Up OAuth Client**:
   - Go to **Profile** -> **OAuth** -> **New Client**.
   - Name it (e.g., `fiii`), and paste the callback URL from your Firefly iii importer instance (e.g., `http://localhost:81/callback`).
   - Uncheck **confidential**.
   - Click on **create** and note down the **Client ID**.

3. **Authorize the App**:
   - Go to your Firefly iii importer, paste the Client ID, and authorize the app.

Once these steps are complete, you can start loading the data into Firefly iii. In your FIYI instance:
1. Click on `Import file`.
2. Select the CSV file you previously exported under `Importable file`.
3. Choose the configuration file `FIYIcfg/mywallet.json` from this repository under `Optional configuration file`.
4. Follow the import steps.

### And Now What?
Once completed, all your data will be imported into Firefly iii. You can use various [Android/iOS apps](https://docs.firefly-iii.org/firefly-iii/other-pages/3rdparty/#mobile-applications) that connect with your Firefly iii instance, replacing MyWallet seamlessly.

I recommend checking out the [Firefly iii documentation](https://docs.firefly-iii.org/), which is thorough and clear.

I've included a function in the code called `get_account_wtransfers()`, which can be handy if you want to work with your MyWallet data, as it allows you to load a single account with all its transactions, including transfers between accounts.

## License
This project is licensed under the MIT License - see the LICENSE file for details.