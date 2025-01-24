import os
import subprocess
import argparse

def polishing(input_folder, threads):
    output_folder = "assembly_results"
    output_folder_path = os.path.join(input_folder, output_folder)
    
    flye_folders = [f for f in os.listdir(output_folder_path) if f.startswith('flye_')]
    for flye_folder in flye_folders:
        assembly_file = os.path.join(output_folder_path, flye_folder, 'assembly.fasta')
        trimm_files = [f for f in os.listdir(input_folder) if f.startswith('trimm_') and f.endswith('.fastq')]

        for trimm_file in trimm_files:
            trimm_file_path = os.path.join(input_folder, trimm_file)
            sam_output = os.path.join(output_folder_path, flye_folder, 'assembly.sam')
            minimap2 = f"minimap2 -a -t {threads} {assembly_file} {trimm_file_path} > {sam_output}"
            subprocess.run(minimap2, shell=True)
            polished_output = os.path.join(output_folder_path, flye_folder, 'polished.fasta')
            racon = f"racon -m 8 -x -6 -g -8 -w 500 -u -t {threads} {trimm_file_path} {sam_output} {assembly_file} > {polished_output}"
            subprocess.run(racon, shell=True)

def qc_assembly(input_folder):
    output_folder = "assembly_results" # Result folder from Flye
    qc_output_folder = "polish_analysis"  # Result folder from QUAST
    
    flye_folders = [f for f in os.listdir(os.path.join(input_folder, output_folder)) if f.startswith('flye_')] # search folder from Flye
    for flye_folder in flye_folders:
        assembly_file = os.path.join(input_folder, output_folder, flye_folder, 'polished.fasta') # Make the path to the input file 
        qc_output_folder_path = os.path.join(input_folder, output_folder, flye_folder, qc_output_folder) # Make the path to the output file 
        
        if not os.path.exists(qc_output_folder_path):
            os.makedirs(qc_output_folder_path) # Make folder
        quast = f"quast.py {assembly_file} -o {qc_output_folder_path}"
        subprocess.run(quast, shell=True)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Polishing assemblies with Minimap2 and Racon.')
    parser.add_argument('--input_path', type=str, required=True, help='Directory path of fastq files to analyze.')
    parser.add_argument('--threads', type=int, default=14, help='Number of threads for polishing.')
   
    args = parser.parse_args()
    polishing(args.input_path, args.threads)
    qc_assembly(args.input_path)



