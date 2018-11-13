import sys
import urllib.request
import re
import os
import os.path
from urllib.error import URLError, HTTPError

search_content = ''

'''
接受用户输入，并根据输入拼接dribble.com图片的路径
然后通过正则获取所有图片地址并下载保存的程序
'''


def showUsage():
    print('使用方式:\n')
    print('添加下面的参数来下载相应格式的图片...\n')
    print('gif 只下载gif图片...\n')
    print('jpg 只下载jpg图片...\n')
    print('png 只下载png图片...\n')


def split_search_content(search_content):
    pat = re.compile(r' *,+[, ]*')

    return pat.split(search_content)


def openurl(url):
    '''
    打开指定的url，并返回请求回来的数据
    '''

    req = urllib.request.Request(url)

    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')

    try:

        html = urllib.request.urlopen(req).read()

    except URLError:

        print('打开链接%s失败...请检查网络链接...' % url)

    return html


def process_url(raw_img_url):
    '''
    处理图片url，去除最后的下划线到后缀的部分，
    这样的图片才是分辨率最高的
    '''

    begin = raw_img_url.rfind('_')

    end = raw_img_url.rfind('.')

    return raw_img_url.replace(raw_img_url[begin:end], '')


def save_img(img_url):
    '''
    下载并保存图片到指定目录
    '''

    print('downloading...', img_url.split('/')[-1])

    try:

        urllib.request.urlretrieve(img_url, img_url.split('/')[-1], None)

    except URLError:

        print('服务器异常...正在再试...')


def get_pics_urls(html):
    '''
    通过正则获取整个本页所有的图片原始url地址，
    并通过process_url()方法对url进行处理
    '''

    urls = pattern.findall(html)

    last_downloading_url = ""

    # 处理过后的url会有很多重复，这里保证相同的url只下载一次
    for each_img_url in urls:

        processed_url = process_url(each_img_url)

        if processed_url != last_downloading_url:
            save_img(processed_url)

            last_downloading_url = processed_url


def download_success_and_count_files():
    '''
    所有文件下载成功之后的提示
    '''

    files = []

    for root, dirs, file in os.walk(os.getcwd()):
        files = file

    print('下载成功！共计%d个文件...' % len(files))

    os.chdir('../..')


def get_dribble_pics(keyword, folder='dribbble', pages=10):
    '''
    切换到指定的保存目录，组装url并开始下载图片
    '''

    if not os.path.exists(folder):
        os.mkdir(folder)

    os.chdir(folder)

    if not os.path.exists(keyword):
        os.mkdir(keyword)

    os.chdir(keyword)

    print('图片保存在：', os.getcwd())

    for page_num in range(pages):
        print('正在下载第%d页...' % (page_num + 1))

        search_query = keyword.replace(' ', '+')

        dribble_page_url = 'http://www.mzitu.com/search?q=' + search_query + '&page=' + str(page_num + 1)

        html = openurl(dribble_page_url).decode('utf-8')

        get_pics_urls(html)

    download_success_and_count_files()


if __name__ == '__main__':
    '''
    编译正则，获取用户输入
    '''
    arg_right = False

    if len(sys.argv) > 1:

        arg = sys.argv[1]

        if arg == 'gif':

            arg_right = True

            pattern = re.compile(r'https://d13yacurqjgara.cloudfront.net/users/\d*/\w*/\d*/.*?\.[g][i][f]')

        elif arg == 'jpg':

            arg_right = True

            pattern = re.compile(r'https://d13yacurqjgara.cloudfront.net/users/\d*/\w*/\d*/.*?\.[j][p][g]')

        elif arg == 'png':

            arg_right = True

            pattern = re.compile(r'https://d13yacurqjgara.cloudfront.net/users/\d*/\w*/\d*/.*?\.[p][n][g]')

        elif arg == 'help':

            arg_right = False

            showUsage()

        else:

            arg_right = False

            showUsage()

    else:

        arg_right = True

        pattern = re.compile(r'https://d13yacurqjgara.cloudfront.net/users/\d*/\w*/\d*/.*?\.[jpg][pni][gf]')

    if arg_right:

        search_content = input('输入要搜索的内容(多个关键字请用英文逗号隔开，输入q或者Q退出):')

        while True:

            keywords = split_search_content(search_content)

            # 如果分割后关键字列表的长度是1
            if len(keywords) == 1:

                first_keyword = keywords[0]

                # 如果这个唯一元素是空字符串，提示重新输入
                if first_keyword == '':

                    search_content = input('没有关键字可以查找，请重新输入：')

                # 如果这个元素是q或者Q，退出程序
                elif first_keyword in ['q', 'Q']:

                    break

                else:

                    get_dribble_pics(first_keyword)

            else:

                for keyword in keywords:
                    get_dribble_pics(keyword)

                break