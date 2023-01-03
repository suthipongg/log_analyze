# README
## How to use
run command : `python3 path/to/log_analyze/main.py -p path/to/log_file.bin -m name_of_model_without_.txt`
example : `python main.py -p "Desktop\log_analyze\log_data\Drone30LOutOfControl.bin" -m 30L`

## Create new moule
1. Create new modules by set the name in lowercase letters.
2. Add all message that required for the new module to dictionary in  `modules/_msgs_module.py`

## Create new model
1. Create new model in .txt format
2. Add modules to be checked line by line.