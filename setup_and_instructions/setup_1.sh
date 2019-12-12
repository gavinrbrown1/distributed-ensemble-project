# Download and install the relevant scripts
echo "Downloading files from Github and unzipping"
wget distributed-ensemble-project-master.zip
unzip distributed-ensemble-project-master.zip
cd distributed-ensemble-project-master

echo "Updating apt-get"
apt-get update

echo "Downloading and installing Anaconda"
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
bash Anaconda3-2019.10-Linux-x86_64.sh

echo "Please restart the shell for Anaconda to take effect"
