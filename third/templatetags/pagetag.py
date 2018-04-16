from django import template
register = template.Library()

from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page,loop_page,num_pages):
    offset = abs(curr_page - loop_page)

    if curr_page==1 or curr_page==num_pages:
        if offset < 5:
            if curr_page == loop_page:
                page_ele = '<li class="active"><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)
            else:
                page_ele = '<li><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)
            return format_html(page_ele)
        else:
            return ''
    elif curr_page==2 or curr_page==num_pages-1:
        if offset < 4:
            if curr_page == loop_page:
                page_ele = '<li class="active"><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)
            else:
                page_ele = '<li><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)
            return format_html(page_ele)
        else:
            return ''
    else:
        if offset < 3:
            if curr_page == loop_page:
                page_ele = '<li class="active"><a href="?page=%s">%s</a></li>'%(loop_page,loop_page)
            else:
                page_ele = '<li><a href="?page=%s">%s</a></li>'%(loop_page,loop_page)
            return format_html(page_ele)
        else:
            return ''