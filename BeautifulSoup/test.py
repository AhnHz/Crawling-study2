import matplotlib.font_manager as fm

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
# OSX 의 설치 된 폰트를 가져오는 함수
#font_list_mac = fm.OSXInstalledFonts()
#print(len(font_list_mac))

f = sorted(f.name for f in fm.fontManager.ttflist)
#f = [(f.name, f.fname) for f in fm.fontManager.ttflist if 'Mal' in f.name]
print(len(font_list))
print(f)