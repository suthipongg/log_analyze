# README
## How to use
run command : `python3 path/to/log_analyze/main.py -p path/to/log_file.bin -m name_of_model_without_.txt`
example : `python main.py -p "Desktop\log_analyze\log_data\Drone30LOutOfControl.bin" -m 30L`

## Create new module
1. Create new modules python format in `modules/`
2. create list that contain all necessary message in "msg" variable (name variable is "msg" only) as global variable in new module python file
3. create analyze log finction (name function is "analyze" only and have only 1 argument is "self") in new module python file
> note : Example module structure in `module/__structure__.py`

## Create new model
1. Create new model .txt format in `models/`
2. Add modules that need to be checked line by line.