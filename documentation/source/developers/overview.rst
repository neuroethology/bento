Overview
========

- Qt and python
    - Experiments Database
    - Timecode
    - Viewers
    - Plug-ins
- Experiments Database
    Various kinds of data related to an experiment are held in a database.  That database can be configured to be either local to the user's workstation, or on a shared database service.  By default, a local, private database is initialized and used.

    - Configuration
        Bento supports configuration information through the :py:class: BentoConfig class, found in db/bentoConfig.py.

    - SQLAlchemy
        - Schema
        - Transactions
    - Investigator
    - Cameras
    - Animal
    -  Session
    -  Trial
    - Video File
    - Pose File
    - Annotations File
    - Neural File
    - Audio File
    - Other File
        The database has provisions for other types of data files in a generic "Other Files" table.  It is not used currently by Bento.

- Time
    - Sources of time
        - Qt timer
        - Media player
- Viewers
    - Main Window
    - Plug-ins
        - Pose
        - Data Export
    - Video
        - Standard formats
        - Proprietary formats
    - Annotations
    - Neural Data (e.g. calcium imaging)
