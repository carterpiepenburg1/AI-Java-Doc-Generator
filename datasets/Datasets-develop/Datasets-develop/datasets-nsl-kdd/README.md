## Knowm Datasets NSL-KDD

[raw data](http://nsl.cs.unb.ca/NSL-KDD/)

Note that the data is no longer available, but it can be accessed as described [here](https://stackoverflow.com/questions/31722843/unable-to-get-nsl-kdd-datasets).

## How to Get the Data

1. Manually download the database files that have been uploaded to Knowm's Google Drive account [here](https://drive.google.com/folderview?id=0ByP7_A9vXm17VXhuZzBrcnNubEE&usp=sharing#list).
1. Manually copy the `DB_NSL_KDD.*` files into the `/usr/local/Datasets` folder. There should be four files. 

## How to Generate Data

1. Download raw data from here: http://nsl.cs.unb.ca/NSL-KDD/
1. put all files (`KDDTrain+.txt` and `KDDTest+.txt`) in `raw` folder in project root
1. Run `RawData2DB.java`. 
1. The database containing the data will appear in `db`.
1. Manually copy the `DB_NSL_KDD.*` files into the `/usr/local/Datasets` folder. There should be three files. 

## Build jar containing Data

## How to Use the Data in You App

1. Put the desired jar on the classpath of your application. This will give you access to the DAO and Bean classes.
1. Just call `init` on the DAO class you are using, passing it the path to the database files that you downloaded or generated above. When finished with the data, call `release`. The following example is for the BreastCancer dataset. For more examples see the `datasets-samples` module. 


    try {
      BreastCancerDAO.init("/usr/local/Datasets/"); // setup data
      BreastCancerDemo demo = new BreastCancerDemo();
      demo.go();
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      BreastCancerDAO.release(); // release data resources
    }
