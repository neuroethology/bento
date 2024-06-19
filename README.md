# The **B**ehavior **E**nsemble and **N**eural **T**rajectory **O**bservatory (Bento)

Bento is a tool for organizing, visualizing, and analyzing multimodal neuroscience datasets.

An earlier, Matlab-based version of Bento is available [here](https://github.com/neuroethology/bentoMAT).

## New In This Release

### Version 0.3.0-beta
#### Added Features
- Plug-ins supporting display of MARS, DLC, and SLEAP pose files
- Support for loading and displaying annotations made in Bento, BORIS, SimBA, and the Caltech Behavior Annotator
- Plug-ins for event-triggered-averaging of neural activity, and for k-means clustering of neurons based on activity over the full trial
- Export of your experimental data (neural recording, pose, behavior annotations) to a NWB file
- Main window now supports jumping to a specific time or frame number in a video
- Added button to delete files from a trial (though you can still also use the delete key)
- Simplified setup of the conda environment, removing OS-specific environment files

#### Bugs Fixed
- Desynced scrolling/display of annotations + neural traces has been fixed
- Editing trials in v0.2.0-beta caused an increment in the trial number; this is now fixed
- Widgets are now cleared out when new data is loaded

## Getting Started

- Please look for the installation instructions at [Installation Instructions](https://github.com/neuroethology/bento/blob/main/documentation/installation.md)
- Please look for the detailed step by step instructions at [Tutorial](https://github.com/neuroethology/bento/blob/main/documentation/tutorial.md)

## Previous Release Updates
### Version 0.2.0-beta
#### Added Features
- A plug-in interface to support import and display of pose data
- A pose plug-in for MARS format mouse pose data
- A pose plug-in for DeepLabCut format generic and MARS-style mouse pose data (*.h5, or *.csv)
- "Parula" color table for display of neural heatmap data
- Annotations can now be applied from the neural viewer window

#### Bugs Fixed
- On initial startup when no Investigators yet exist, v0.1.0-beta would prompt for the selection of an Investigator anyway.
With this release, it takes you to the "Add Investigators" dialog instead.
- The vertical scaling of annotations has been fixed.

## Citation

## License

## Contact
