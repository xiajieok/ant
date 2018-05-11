from django import template
from django.utils.html import format_html
import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def guess_page(current_page, loop_num):
    offset = abs(current_page - loop_num)
    if offset < 5:
        if current_page == loop_num:
            page_ele = '''<li class="active"><a href="?page=%s">%s</a></li>''' % (loop_num, loop_num)
        else:
            page_ele = '''<li ><a href="?page=%s">%s</a></li>''' % (loop_num, loop_num)
        return format_html(page_ele)
    else:
        return ''

@register.filter
def more(value, post_id):
    """通过[!--more--]标签实现文章截取和增加查看全文链接"""
    more_str = '[!--more--]'
    if more_str in value:
        return value.split(more_str)[0] + '<a href="/post/{0}">查看全文...</a>'.format(post_id)
    return value

@register.filter
def sum_size(data_set):
    total_val = sum([i.capacity if i.capacity else 0 for i in data_set])
    # res = int(total_val/1024)
    return total_val
# register = template.Library()  # 自定义filter时必须加上
#
#
# @register.filter(is_safe=True)  # 注册template filter
# @stringfilter  # 希望字符串作为参数
# def custom_markdown(value):
#     return mark_safe(markdown.markdown(value,
#                                        extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],
#                                        safe_mode=True,
#                                        enable_attributes=False))
