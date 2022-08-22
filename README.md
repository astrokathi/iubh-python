# iubh-python
Python Assignment to find the number of ideal functions that can be mapped to the provided test dataset.

# Cloning the repository
Assuming that git is installed in the Machine/ System, follow the below commands to checkout the code.
Please setup a Personal Access Token in GITHUB developer settings as the PAT will be used in place of password for performing actions on the remote using HTTPS.

Checkout:
```
git clone https://github.com/astrokathi/iubh-python.git
cd iubh-python
pip install -r requirements.txt
```

Creating a new branch:
```
git checkout -b mybranch  (this will pull the latest changes from develop and then create a new branch called mybranch)
// do some changes in the files.
git add <filepath1> <filepath2> (file paths of the changed files)
git status (this is to check how many files are untracked, modified and staged, the files added from the above step will hightlight in green)
git commit -m "Commit message - briefing out the features modified or enhanced"
git push (if it doesn't push, set the upstream pointing to origin/mybranch) [execute the provided error message in the terminal]
```
Once the changes are pushed to the custom branch, a pull request has to be raised from the github website, which will then be reviewed by the owner of the repository and will be merged to the develop branch.
To merge the branch to develop using git commands, follow the below commands.

```
git checkout develop (make sure that you are in the develop branch)
git fetch origin (to pull the changes from the origin to the remote)
git pull (to update all the latest changes in the develop branch)
git merge mybranch (this will merge all the changes from mybranch to develop)[This will happen only when permission provided to merge branches to develop]
```


# Pre-requisites
It is assumed that python3 is already installed.

# Setup
`pip install -r requirements.txt`
This will install all the dependencies need to run this project.


# Notes:
In the code, the parameter `plot` has to be set to *True* in order to plot the Graphs in the project.
