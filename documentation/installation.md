# Installation

Bento requires Python version XX or above, and can be run on Windows, MacOS, or Linux.

**Follow the instructions below to install GuPPy :** <br>

1. Download the Bento code.<br>

2. Install [Anaconda](https://www.anaconda.com/products/individual#macos). Install Anaconda based on your operating system (Mac, Windows or Linux) by following the prompts when you run the downloaded installation file.

3. Once installed, open an Anaconda Prompt window (for windows) or Terminal window (for Mac or Linux). 

4. Find the location where Bento folder is located and execute the following command on the Anaconda Prompt or terminal window: 

```
cd path_to_bento_folder
```
	- Ex : cd /Users/KennedyLab/all_codes/bento

5. Execute the following command to install all the dependencies/packages required for Bento.<br>
   - Note : filename in the command should be replaced by <b>bento_windows.yml</b> or <b>bento_mac.yml</b> or <b>bento_ubuntu.yml</b> (based on your OS) <br>

```
conda env create -f filename
```

6. Execute the following two commands to open the Bento User Interface:

```
conda activate bento
python src/bento.py
```
