# from bs4 import BeautifulSoup
import re

cheatsheet = open("cheatsheet.txt", "rb").read().decode()

re_fa = re.compile("      fa(.*)")
re_ch = re.compile("\[&amp;#x(.*?);\]")

fas = re.findall(re_fa, cheatsheet)  # ['-500px\r', '-address-book\r']
chs = re.findall(re_ch, cheatsheet)  # ['f26e', 'f2b9']
assert len(fas) == len(chs)

with open("result.txt", "w") as fp:
    for i in range(len(fas)):
        fp.write('fa{0} = "\\u{1}"'.format(
            fas[i].replace("\r", "").replace("-", "_"),
            chs[i])
        )
        fp.write("\n")
print("ok")

# bs = BeautifulSoup(cheatsheet)
#
# divs = bs.find_all("div", {"class":"col-print-4"})
#
# with open("result.txt","w") as fp:
#     for div in divs:
#         s = [repr(ss).replace("\\u","#") for ss in div.stripped_strings]
#         print(s)
#         if len(s)==3:
#             fp.write('{1} = "{0}"'.format(*s))
#         else:
#             fp.write('{2} = "{1}"'.format(*s))
#         fp.write("\n")
# print("ok")
# print(list(divs[0].stripped_strings))
# >> ['4.4', '\uf26e', 'fa-500px', '[&#xf26e;]']
