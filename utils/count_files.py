import os

def count_pdfs(dir):
    # input a folder 
    # output the number of pdfs in the folder including subfolders
    count = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".pdf"):
                count += 1

    return count

if __name__ == "__main__":
    print(count_pdfs("output_files"))  # Output: 0
