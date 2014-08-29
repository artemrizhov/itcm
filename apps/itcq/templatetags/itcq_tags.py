from django import template

register = template.Library()

@register.inclusion_tag('itcq/sponsors.html')
def sponsors():
    from itcq.models import Sponsor
    return {"sponsor_list": Sponsor.objects.all()}

@register.inclusion_tag('cms/content.html', takes_context=True)
def ancestor_title(context, level=0, var=None):
    request = context['request']
    page = request.current_page

    if page:
        ancestors = [page]
        while ancestors[-1].parent:

            ancestors.append(ancestors[-1].parent)
        ancestors.reverse()
        if len(ancestors) <= level:
            return {"content": ""}
        if var:
            context[var] = ancestors[level].get_menu_title()
            return {"content": ""}
        else:
            return {"content": ancestors[level].get_menu_title()}
    else:
        return {"content": ""}

@register.inclusion_tag('cms/content.html', takes_context=True)
def ancestor_slug(context, level=0):
    request = context['request']
    page = request.current_page
    if page:
        ancestors = [page]
        while ancestors[-1].parent:
            ancestors.append(ancestors[-1].parent)
        ancestors.reverse()
        if len(ancestors) <= level:
            return {"content": ""}
        return {"content": ancestors[level].get_slug()}
    else:
        return {"content": ""}
