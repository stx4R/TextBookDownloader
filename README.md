# TextBookDownloader

위 프로그램은 교과서 웹앱 뷰어에서 PDF 파일을 찾은 후 결과값을 가공하여 이미지 파일을 전부 다운받는 형식으로 작동됩니다.

출판사마다 웹앱 PDF 경로의 접근 방식이 다르니 각각의 방식을 아래에 서술합니다.
출판사마다 프로그램이 (불)필요한 경우가 있습니다.

# 프로그램 가동 필요
천재교과서 : F12(F5) -> Network -> Fetch/XHR -> Ctrl + L -> 스크롤 -> 새로 생긴 파일 중 'N?zoom=NN&jpegQuality=o& .....'의 Copy URL -> 프로그램 가동(경로 필요)
동아출판   : F12(F5) -> Network -> s001.jpg or 001.jpg의 경로 복사 -> 프로그램 가동(경로 필요)  
# 프로그램 가동 불필요
미래엔    : F12(F5) -> Console -> PDFViewerApplication.url 타이핑
