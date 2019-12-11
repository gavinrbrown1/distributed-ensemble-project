echo "Installing pytorch"
conda install pytorch torchvision cpuonly -c pytorch

echo "Downloading files from Github and unzipping"
unzip distributed-ensemble-project-master.zip
cd distributed-ensemble-project-master
