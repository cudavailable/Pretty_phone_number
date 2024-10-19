"""
# 根据用户需要，分页展示 ###########################

    query_set = models.PrettyNum.objects.filter(**dict_list).order_by('-level')  # 从数据库中取出所需要的记录，传递给分页组件
    page_obj = pagiantion(request, query_set, pagenum=6)   # 实例化分页组件

    # 获取分页结果
    (prev_page, page_string, post_page) = page_obj.html()

    # 传递给前端的参数配置
    context = {
        "query_set": page_obj.query_set, "search_data": search_data, "page_string": page_string,
        "prev_page": prev_page, "post_page": post_page
    }

    # query_set = models.PrettyNum.objects.all().order_by('-level')  # select * from app01_prettynum order by level desc
    return render(request, 'pretty_list.html', context)

# HTML 显示
    # 分页
    <ul class="pagination" style="float: left;">
        {{page_string}}
    </ul>

    # 查询结果前端循环展示
    {% for obj in query_set %}
        <th scope="row">{{obj.id}}</th>
        <td>{{obj.mobile}}</td>
    {% endfor %}
"""

from django.utils.safestring import mark_safe
import copy
class pagiantion:
    """封装分页组件"""
    def __init__(self, request, query_set, pagenum=4, page_param='page', offset=2):
        query_dict = copy.deepcopy(request.GET)  # 深拷GET的参数
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            # 如果请求的page不是数字，则默认值为1
            page = 1

        self.page = page    # 获取到请求的页面
        self.start = (page - 1) * pagenum  # 起始页面的数据索引
        self.end = page * pagenum  # 终止页面的数据索引
        self.query_set = query_set[self.start:self.end]
        len_data = query_set.count()
        total_page, div = divmod(len_data, pagenum)
        if div > 0:
            total_page += 1
        self.total_page = total_page
        self.offset = offset  # 显示的是前后各2个页面

    def html(self):
        start_page = max(self.page - self.offset, 1)  # 起始页面号
        end_page = min(self.page + self.offset, self.total_page)  # 终止页面号

        # 显示所有的页
        page_str_list = []
        prev_page = max(self.page - 1, 1)
        self.query_dict.setlist(self.page_param, [prev_page])
        prev = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                # 如果是当前页的话，强调一下
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        post_page = min(self.page + 1, self.total_page)
        if post_page == 0:
            """后一页不能为0"""
            post_page = 1
        self.query_dict.setlist(self.page_param, [post_page])
        post = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
        page_str_list.append(post)

        page_string = mark_safe("".join(page_str_list))

        return page_string