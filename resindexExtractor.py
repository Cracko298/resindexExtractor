import sys, os
with open(sys.argv[1], 'rb+') as f:
    header = f.read(0x04); bDir = ".\\outChunks"; data = len(f.read()); f.seek(0x04); os.makedirs(bDir, exist_ok=True); file_index = 0
    chunkCounter = 0; dataCounter = 0
    for i in range(int(data/4)):
        chunk = f.read(4)
        if len(chunk) < 4:
            break
                
        folder_name = f"{chunk[-1]:02X}"
        folder_path = os.path.join("outChunks", folder_name)                
        os.makedirs(folder_path, exist_ok=True)
        file_name = f"{file_index:08X}.bin"
        with open(os.path.join(folder_path, file_name), 'wb') as out_file:
            out_file.write(chunk)
                
        file_index += 1; print(f"Extracted Data from {sys.argv[1]} into {file_name}");dataCounter += 1

    for folder_name in os.listdir(bDir):
        folder_path = os.path.join(bDir, folder_name)
        
        if os.path.isdir(folder_path):  # Ensure it's a directory
            combined_file_name = f"chunk_{folder_name.zfill(8)}.bin"
            combined_file_path = os.path.join(folder_path, combined_file_name)

            # Open the combined file for writing
            with open(combined_file_path, 'wb') as combined_file:
                # Iterate through each file in the folder
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path) and file_name != combined_file_name:
                        # Append the content of each file to the combined file
                        with open(file_path, 'rb') as input_file:
                            combined_file.write(input_file.read())

            print(f"Extracted Chunk from {sys.argv[1]} into {combined_file_name}"); chunkCounter += 1
    
    with open(f".\\outChunks\\header.bin", 'wb') as f:
        f.write(header)

    print(f"Extracted Header from {sys.argv[1]} to header.bin")
    print(f"Amount of Data: {dataCounter}\nAmount of Chunks: {chunkCounter}")