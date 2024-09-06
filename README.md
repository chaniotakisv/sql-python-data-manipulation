Installation and usage instructions
    
    • Open the python file chaniotakis_sql_python_data_manipulation.py and assign your local machine's input_directory at line 7 (changing the path where input.ini is located).
      
    • On line 84, we assign the output path tsv_file_path where we want the file containing the collected information to be stored on our local machine.
      
    • Then, we save and close the chaniotakis_sql_python_data_manipulation.py file.
      
    • We open a terminal on our operating system and navigate to the folder where the chaniotakis_sql_python_data_manipulation.py file is located.
      
    • Next, we type python3 chaniotakis_sql_python_data_manipulation.py to execute the code in Python 3.
      
    • We observe that it will print the information collected from the Ensembl API regarding Human Gene, ID, Mouse Gene ID, and Percent Identity in correspondence with the order read from the .ini file, and it informs us in case it doesn't find any ortholog.
      
    • Afterwards, the code will export a file named coding_test.tsv containing the information requested by the use case exactly as presented in the example_output.tsv example.
    
    documentation link 1: https://rest.ensembl.org/
    
    documentation link 2: https://genome.ucsc.edu/goldenPath/help/mysql.html
