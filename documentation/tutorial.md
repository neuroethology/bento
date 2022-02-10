# Tutorial
This tutorial will walk you through the entire process of setting up Bento and working with data. Follow this tutorial using our sample dataset, then get started with your own data.

> ANN: once I've written this part, each ## header should be split into its own separate file within the tutorial folder, and the text below replaced with a hyperlinked table of contents.

## Initializing Bento
These steps will need to be followed the first time you run Bento.

### Before you begin
Bento constructs a database that keeps track of your data files. You can choose to manage data in two ways: in a local, private database or via a shared database.

- **Private** database hosting allows you to quickly install and start using Bento without installing additional software, however the built database cannot be easily shared by multiple users within a lab.
- **Shared** database hosting allows you to create a common lab-wide database to manage your group's experimental data. This configuration requires some additional effort to set up hosting on a server or network-attached storage device.

### Setting up a private database

### Setting up a shared database

## Preparing the database
Before you can start adding actual experiments, you'll need to provide a little background information for the database.

### Adding investigators

1. Click on **Database** in the menu bar and then click on **Investigator...** option. **Investigator Dialog** will pop up.
2. Select **New Investigator** in the **Investigator** field.
3. Type relevant information in all the fields and hit **Apply** button.
4. After hitting **Apply** button, you can see an investigator information popping up when you select the added investigator.
5. You can add multiple investigators based on your requirement. Repeat steps 1-4, every time you need to add a new investigator.

![alt-text](../_gifs/adding_investigator.gif)

### Adding animals

1. Click on **Database** in the menu bar and then click on **Animal...** option. **Animal Dialog** will pop up.
2. Select relevant investigator in the **Investigator** field.
3. In the **Animal** table, click on the first row which says **New Animal**.
4. Add information such as **Animal Services ID**, **Nickname**, **Date of Birth**, **Sex** and **Genotype**.
5. Click on **Apply** button and you will see new animal in the **Animal** table.
6. You can add multiple animals based on your requirement. Repeat steps 1-5, every time you need to add a new animal.

#### Tracking animal surgeries

1. In the **Animal Dialog**, you can see section called **Surgical Log** at the bottom. You can add surgical logs for each animal added. 
2. Select an added animal in the **Animal** table.
3. Click on **Add ...** button located in the **Surgical log** section. **Add Surgery Dialog** will pop up.
4. Add all the information in the dialog and click on **OK** button.
5. Repeat steps 1-4, every time you need to add a new surgical log.

### Adding camera profiles

1. Click on **Database** in the menu bar and then click on **Camera...** options. **Camera Dialog** will pop up.
2. Select **New Camera** in the **Camera** field.
3. Type relevant information in the all the fields and hit **Apply** button.
4. After hitting **Apply** button, you can see camera information popping up when you select the added camera.
5. You can add multiple cameras based on your requirement. Repeat steps 1-4, every time you need to add a new camera.


## Populating the database
Now that you have experimenters, animals, and cameras on record, you can start using Bento to organize your experimental data.

### Adding a Session

### Adding and populating a Trial

### Syncing up multiple data files

## Loading data from a trial

## Annotating a trial

### Creating a new annotation channel

### Creating a new behavior

### Editing behavior properties

### Adding annotations

### Deleting annotations

### Saving annotations
