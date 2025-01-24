import os
import subprocess
import argparse

def cq_first(input_folder, threads):

    output_folder = "fastqc_results"    # Result folder from FastQC
    output_folder_path = os.path.join(input_folder, output_folder) # Make the path to the output folder
    if not os.path.exists(output_folder_path):  # Make folder
        os.makedirs(output_folder_path)
        
    files = [f for f in os.listdir(input_folder) if f.endswith('.fastq') or f.endswith('.fastq.gz')] # search for files with .fastq or .fastq.gz format
    for file in files:
        file_path = os.path.join(input_folder, file)  # Make the path to the input file
        fastqc = f"fastqc -t {threads} -o \"{output_folder_path}\" \"{file_path}\""
        subprocess.run(fastqc, shell=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Execute FastQC.')
    parser.add_argument('--input_path', type=str, required=True, help='Directory path of fastq or fastq.gz files to analyze.')
    parser.add_argument('--threads', type=int, default=14, help='Number of threads for FastQC.')

    args = parser.parse_args()  
    cq_first(args.input_path, args.threads)
