

# 위 프로그램은 교과서 웹앱 뷰어에서 PDF 파일을 찾은 후 결과값을 가공하여 이미지 파일을 전부 다운받는 형식으로 작동됩니다.

# 출판사마다 웹앱 PDF 경로의 접근 방식이 다르니 각각의 방식을 아래에 서술합니다.
# 출판사마다 프로그램이 (불)필요한 경우가 있습니다.

# 프로그램 가동 필요
#// 천재교과서 : F12(F5) -> Network -> Fetch/XHR -> Ctrl + L -> 스크롤 -> 새로 생긴 파일 중 'N?zoom=NN&jpegQuality=o& .....'의 Copy URL -> 프로그램 가동(경로 필요)
# 동아출판   : F12(F5) -> Network -> s001.jpg or 001.jpg의 경로 복사 -> 프로그램 가동(경로 필요)  
# 프로그램 가동 불필요
# 미래엔    : F12(F5) -> Console -> PDFViewerApplication.url 타이핑

import requests
import os
import re
import img2pdf  

print("------------------------------------------------")
print("📚 TextbookDownloader v1.1")
print("------------------------------------------------")

subject_name = input("1. 저장할 이름을 입력하세요. (다운받을 이미지의 폴더명을 설정합니다.): ")

print("2. 고유 url의 첫 페이지 주소를 삽입하세요.")
print("   (예: https://.../2375/s001.jpg)")
full_url = input("   주소 붙여넣기: ").strip()

try:
    filename = full_url.split('/')[-1]
    base_url = full_url.replace(filename, "")
    match = re.match(r"([a-zA-Z_-]*)(\d+)(\.[a-zA-Z]+)", filename)
    if not match:
        raise ValueError("주소 형식이 올바르지 않습니다. .jpg로 끝나는지 확인해주세요.")
    prefix = match.group(1)
    start_num_str = match.group(2)
    extension = match.group(3)
    padding_len = len(start_num_str)
    page_num = int(start_num_str)
    print(f"\n 주소 분석 성공")
    print(f"   - 패턴: '{prefix}' + 숫자({padding_len}자리) + '{extension}'")
    print(f"   - 시작: {page_num}페이지부터")

except Exception as e:
    print(f"\n 주소 분석 실패: {e}")
    print("이미지 주소가 올바르지 않습니다.")
    exit()

root_folder = "textbook_images"
target_folder = os.path.join(root_folder, subject_name)

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

print(f"\n'{subject_name}' 다운로드를 시작합니다...")

downloaded_files = []

while True:
    current_filename = f"{prefix}{str(page_num).zfill(padding_len)}{extension}"
    download_url = base_url + current_filename
    
    try:
        response = requests.get(download_url, timeout=10)
        
        if response.status_code == 200:
            save_path = os.path.join(target_folder, current_filename)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            downloaded_files.append(save_path)

            if page_num % 10 == 0:
                print(f"   - {page_num}페이지까지 완료됨. ( 10배수마다 표기 ) ({current_filename})")
            page_num += 1
        else:
            print(f"\n다운로드 종료 (마지막 파일: {prefix}{str(page_num-1).zfill(padding_len)}{extension})")
            break
            
    except Exception as e:
        print(f"에러 발생: {e}")
        break

if downloaded_files:
    print("\n🔄 PDF 변환 중... (잠시만 기다려주세요)")
    
    pdf_filename = f"{subject_name}.pdf"
    pdf_path = os.path.join(target_folder, pdf_filename)
    
    try:
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(downloaded_files))
            
        print(f"⭕ PDF 변환 성공")
        print(f"📂 저장 위치: {pdf_path}")
        
    except Exception as e:
        print(f"❌ PDF 변환 실패: {e}")
        print("참고: 이미지 파일이 손상되었거나 호환되지 않는 형식일 수 있습니다.")
else:
    print("\n⚠️ 다운로드된 이미지가 없어 PDF를 생성하지 않았습니다.")

input("\n종료하려면 엔터키를 누르세요...")