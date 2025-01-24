import os
import subprocess
import argparse

def trimming(input_folder):

    files = [f for f in os.listdir(input_folder) if f.endswith('.fastq') or f.endswith('.fastq.gz')] # search for files with .fastq or .fastq.gz format
    for file in files:   # Define name base
        if file.endswith('.fastq.gz'):
            name_sample = file[:-9]  # Remove '.fastq.gz'
        else:
            name_sample = file[:-6]  # Remove '.fastq'
        
        file_path = os.path.join(input_folder, file)  # Make the path to the input file 
        output_path = os.path.join(input_folder, f"trimm_{name_sample}.fastq")  # Make the path to the output file with new name
        porechop = f"porechop -i \"{file_path}\" -o \"{output_path}\""
        subprocess.run(porechop, shell=True)

def cq_sec(input_folder, threads):

    output_folder = "fastqc_results"    # Result folder from FastQC
    output_folder_path = os.path.join(input_folder, output_folder) # Make the path to the output folder
    
    files_trimm = [f for f in os.listdir(input_folder) if f.startswith('trimm_') and f.endswith('.fastq')] # search for files with .fastq or .fastq.gz format
    for file in files_trimm:
        file_path = os.path.join(input_folder, file)  # Make the path to the input file
        fastqc = f"fastqc -t {threads} -o \"{output_folder_path}\" \"{file_path}\""
        subprocess.run(fastqc, shell=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Execute trimming and FastQC.')
    parser.add_argument('--input_path', type=str, required=True, help='Directory path of fastq or fastq.gz files to analyze.')
    parser.add_argument('--threads', type=int, default=14, help='Number of threads for FastQC.')

    args = parser.parse_args()
    trimming(args.input_path)  
    cq_sec(args.input_path, args.threads)

