DIR="venv"
if [[ ! -d $DIR ]] ; then
   echo "Setting up virtual env"
   virtualenv venv
fi
echo "Activating Virtual Environment"
source venv/bin/activate
echo "Installing Packages"
pip install -r tfmodelserver/requirements.txt
pip install -r http-server/requirements.txt
pip install -e git+https://github.com/tensorflow/models.git#egg=subpkg\&subdirectory=research
