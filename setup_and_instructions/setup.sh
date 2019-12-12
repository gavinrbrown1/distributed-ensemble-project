# Download and install the relevant scripts
echo "Downloading files from Github and unzipping"
wget https://github.com/gavinrbrown1/distributed-ensemble-project/archive/master.zip
unzip master.zip

echo "Updating apt-get"
apt-get update

echo "Downloading and installing Anaconda"
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
bash Anaconda3-2019.10-Linux-x86_64.sh

echo "Please restart the shell for Anaconda to take effect"
