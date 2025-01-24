import os
import subprocess
import argparse

def assembly(input_folder, threads):
    output_folder = "assembly_results" # Result folder from Flye
    output_folder_path = os.path.join(input_folder, output_folder) # Make the path to the output folder
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path) # Make folder
        
    files_trimm = [f for f in os.listdir(input_folder) if f.startswith('trimm_') and f.endswith('.fastq')] # search for files
    for file in files_trimm:
        name_sample = file[len('trimm_'):-len('.fastq')] # Define name base folder
        output_dir = os.path.join(output_folder_path, f"flye_{name_sample}") # Make the path to the output file
        flye = f"flye --nano-raw {os.path.join(input_folder, file)} --out-dir {output_dir} --threads {threads}"  
        subprocess.run(flye, shell=True)
        
def qc_assembly(input_folder):
    output_folder = "assembly_results" # Result folder from Flye
    qc_output_folder = "quast_analysis"  # Result folder from QUAST
    
    flye_folders = [f for f in os.listdir(os.path.join(input_folder, output_folder)) if f.startswith('flye_')] # search folder from Flye
    for flye_folder in flye_folders:
        assembly_file = os.path.join(input_folder, output_folder, flye_folder, 'assembly.fasta') # Make the path to the input file 
        qc_output_folder_path = os.path.join(input_folder, output_folder, flye_folder, qc_output_folder) # Make the path to the output file 
        
        if not os.path.exists(qc_output_folder_path):
            os.makedirs(qc_output_folder_path) # Make folder
        quast = f"quast.py {assembly_file} -o {qc_output_folder_path}"
        subprocess.run(quast, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute Flye and QUAST.')
    parser.add_argument('--input_path', type=str, required=True, help='Directory path of fastq files to analyze.')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads for Flye.')
   
    args = parser.parse_args()
    assembly(args.input_path, args.threads)
    qc_assembly(args.input_path)




