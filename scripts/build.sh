# This file is used after the setup and for subsequent builds
python3 -m venv venv
source venv/bin/activate
conda deactivate
python3 -m pip install --upgrade pip
pip install -r requirement.txt


