# from parent directory

git --version
git config --global user.name daisyLsbu
git config --global user.email mymail.daisy@gmail.com
git clone <>
# git init 
git pull  
git add .
git commit -m 'test commit'
git pull  
git push -u origin main

copy commit file
setup git_ignore for venv, data and commit file
python3 -m venv venv
conda deactivate
source venv/bin/activate

python3 -m pip install --upgrade pip

# for checking in different repo and new branch
source venv/bin/activate
conda deactivate 
git remote add master https://github.com/daisyLsbu/MigrationOrchestrator.git
git checkout -b orchestrator

git remote -v 
git pull origin main
git add . 
git commit -m "fist" 
git pull origin main 
git push -u origin main
--
git push -u master orchestrator
