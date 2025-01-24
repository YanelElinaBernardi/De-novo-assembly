import os
import subprocess
import argparse

def concatenate(input_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith('.fastq') or f.endswith('.fastq.gz')]
    samples = set()  # Set for save unique names
    for file in files:
        if file.endswith('.fastq.gz'):
            name_sample = file[:-9]  # Remove '.fastq.gz'
        else:
            name_sample = file[:-6]  # Remove '.fastq'
        samples.add(name_sample)

    for sample in samples:
        files_concat = [os.path.join(input_folder, f) for f in files if f.startswith(sample)] # Find and concatenate the files that correspond to each sample.
        output_file = os.path.join(input_folder, f"{sample}_merge.fastq.gz")
        concatenate = f"cat {' '.join(files_concat)} > {output_file}"
        subprocess.run(concatenate, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate the files that correspond to each sample.')
    parser.add_argument('--input_path', type=str, required=True, help='Directory path of fastq or fastq.gz files to analyze.')
    
    args = parser.parse_args()
    concatenate(args.input_path)

