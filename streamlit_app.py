import streamlit as st
import os

def write_code_to_file(folder_path):
    folder_name = os.path.basename(folder_path)
    output_file_index = 1
    output_file_path = os.path.join(folder_path, f"{folder_name}_0{output_file_index}.txt")
    max_file_size = 3 * 1024 * 1024  # 3 MB
    excluded_files = {'.next', 'node_modules', 'components/ui', '.json', '.gitignore', 'next-env.ts', 'next.config.js', 'README.md', '.txt'}
    extensions = {'.tsx', '.ts', '.js', '.jsx'}
    file_count = 0
    total_files = 0

    def create_new_file():
        nonlocal output_file_index, output_file_path, output_file
        output_file_index += 1
        output_file_path = os.path.join(folder_path, f"{folder_name}_0{output_file_index}.txt")
        output_file = open(output_file_path, 'w', encoding='utf-8')

    output_file = open(output_file_path, 'w', encoding='utf-8')
    
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_files]
        total_files += len(files)
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                output_file.write(f'// 파일 상대 경로: {os.path.relpath(file_path, folder_path)}\n')
                with open(file_path, 'r', encoding='utf-8') as code_file:
                    code_content = code_file.read()
                    output_file.write(code_content + '\n\n')
                
                file_count += 1
                if output_file.tell() > max_file_size:
                    output_file.close()
                    create_new_file()
    
    output_file.close()
    return total_files, file_count

st.title('코드 파일 기록기')

folder_path = st.text_input("폴더 경로를 입력하세요:")

if st.button('실행'):
    if folder_path:
        if os.path.exists(folder_path):
            total_files, recorded_files = write_code_to_file(folder_path)
            st.success(f"처리 완료!")
            st.info(f"총 {total_files}개의 파일이 있습니다.")
            st.info(f"총 {recorded_files}개의 파일을 기록했습니다.")
        else:
            st.error("입력한 폴더 경로가 존재하지 않습니다.")
    else:
        st.warning("폴더 경로를 입력해주세요.")
