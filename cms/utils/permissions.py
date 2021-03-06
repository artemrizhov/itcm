from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from cms.models import Page, PagePermission, GlobalPagePermission
from cms.exceptions import NoPermissionsException
from cms import settings as cms_settings
from django.contrib.sites.models import Site
from sets import Set

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

# thread local support
_thread_locals = local()

def set_current_user(user):
    """Assigns current user from request to thread_locals, used by
    CurrentUserMiddleware.
    """
    _thread_locals.user=user

    
def get_current_user():
    """Returns current user, or None
    """
    return getattr(_thread_locals, 'user', None)


def has_page_add_permission(request):
    """Return true if the current user has permission to add a new page. This is
    just used for general add buttons - only superuser, or user with can_add in
    globalpagepermission can add page.
    
    
    Special case occur when page is going to be added from add page button in
    change list - then we have target and position there, so check if user can
    add page under target page will occur. 
    """        
    opts = Page._meta
    if request.user.is_superuser or \
        (request.user.has_perm(opts.app_label + '.' + opts.get_add_permission()) and
            GlobalPagePermission.objects.with_user(request.user).filter(can_add=True)):
        return True
    
    # if add under page
    target = request.GET.get('target', None)
    position = request.GET.get('position', None)
    
    if target is not None:
        try:
            page = Page.objects.get(pk=target)
        except:
            return False
        if position == "first-child":
            return page.has_add_permission(request)
        elif position in ("left", "right"):
            return has_add_page_on_same_level_permission(request, page)
    return False

    
def get_user_permission_level(user):
    """Returns highest user level from the page/permission hierarchy on which
    user haves can_change_permission. Also takes look into user groups. Higher 
    level equals to lover number. Users on top of hierarchy have level 0. Level 
    is the same like page.level attribute.
    
    Example:
                              A,W                    level 0
                            /    \
                          user    B,GroupE           level 1
                        /     \
                      C,X     D,Y,W                  level 2
        
        Users A, W have user level 0. GroupE and all his users have user level 1
        If user D is a member of GroupE, his user level will be 1, otherwise is
        2.
    
    """
    if user.is_superuser or \
        GlobalPagePermission.objects.with_can_change_permissions(user).count():
        # those
        return 0
    try:
        permission = PagePermission.objects.with_can_change_permissions(user).order_by('page__level')[0]
    except IndexError:
        # user is'nt assigned to any node
        raise NoPermissionsException
    return permission.page.level

def get_subordinate_users(user):
    """Returns users queryset, containing all subordinate users to given user 
    including users created by given user and not assigned to any page.
    
    Not assigned users must be returned, because they shouldn't get lost, and
    user should still have possibility to see them. 
    
    Only users created_by given user which are on the same, or lover level are
    returned.
    
    If user haves global permissions or is a superuser, then he can see all the
    users.
    
    This function is currently used in PagePermissionInlineAdminForm for limit
    users in permission combobox. 
    
    Example:
                              A,W                    level 0
                            /    \
                          user    B,GroupE           level 1
                Z       /     \
                      C,X     D,Y,W                  level 2
                      
        Rules: W was created by user, Z was created by user, but is not assigned
        to any page.
        
        Will return [user, C, X, D, Y, Z]. W was created by user, but is also
        assigned to higher level.
    """
    
    # TODO: try to merge with PagePermissionManager.subordinate_to_user()
    
    if user.is_superuser or \
            GlobalPagePermission.objects.with_can_change_permissions(user):
        return User.objects.all() 
    
    page_id_allow_list = Page.permissions.get_change_permissions_id_list(user)
    
    user_level = get_user_permission_level(user)
    
    qs = User.objects.distinct().filter(
        Q(is_staff=True) &
        (Q(pagepermission__page__id__in=page_id_allow_list) & Q(pagepermission__page__level__gte=user_level)) 
        | (Q(pageuser__created_by=user) & Q(pagepermission__page=None))
    )
    qs = qs.exclude(pk=user.id).exclude(groups__user__pk=user.id)
    return qs

def get_subordinate_groups(user):
    """Simillar to get_subordinate_users, but returns queryset of Groups instead
    of Users.
    """
    if user.is_superuser or \
            GlobalPagePermission.objects.with_can_change_permissions(user):
        return Group.objects.all()
    
    page_id_allow_list = Page.permissions.get_change_permissions_id_list(user)
    user_level = get_user_permission_level(user)
    
    qs = Group.objects.distinct().filter(
         (Q(pagepermission__page__id__in=page_id_allow_list) & Q(pagepermission__page__level__gte=user_level)) 
        | (Q(pageusergroup__created_by=user) & Q(pagepermission__page=None))
    )
    return qs

def has_global_change_permissions_permission(user):
    opts = GlobalPagePermission._meta
    if user.is_superuser or \
        (user.has_perm(opts.app_label + '.' + opts.get_change_permission()) and
            GlobalPagePermission.objects.with_user(user).filter(can_change=True)):
        return True
    return False

def has_add_page_on_same_level_permission(request, page):
    """Checks if there can be page added under page parent.
    """
    if not cms_settings.CMS_PERMISSION or request.user.is_superuser \
        or GlobalPagePermission.objects.with_user(request.user).filter(can_add=True).count():
        return True
    try:
        return has_generic_permission(page.parent_id, request.user, "add")
    except AttributeError:
        # if page doesnt have parent...
        pass
        """
        if page.level == 0:
            # we are in the root, check if user haves add PAGE paermisson for
            # this page
            for perm in PagePermission.objects.with_user(request.user).filter(page=page, can_add=True):
                if perm.grant_on & MASK_PAGE:
                    print PagePermission.objects.with_user(request.user).filter(page=page, can_add=True)
                    return True
        """ 
    return False

def mail_page_user_change(user, created=False, password=""):
    """Send email notification to given user. Used it PageUser profile creation/
    update.
    """
    from cms.utils.mail import send_mail
    
    if created:
        subject = _('CMS - your user account was created.')
    else:
        subject = _('CMS - your user account was changed.')
    
    context = {
        'user': user,
        'password': password or "*" * 8,
        'created': created,
    }
    send_mail(subject, 'admin/cms/mail/page_user_change.txt', [user.email], context, 'admin/cms/mail/page_user_change.html')


def has_generic_permission(page_id, user, attr):
    """Permission getter for single page with given id.
    """    
    func = getattr(Page.permissions, "get_%s_id_list" % attr)
    permission = func(user)
    return permission == Page.permissions.GRANT_ALL or page_id in permission


def get_user_sites_queryset(user):
    """Returns queryset of all sites available for given user.
    
    1.  For superuser always returns all sites.
    2.  For global user returns all sites he haves in global page permissions 
        together with any sites he is assigned to over an page.
    3.  For standard user returns just sites he is assigned to over pages.
    """
    qs = Site.objects.all()
    
    if user.is_superuser:
        return qs
    
    global_ids = GlobalPagePermission.objects.with_user(user) \
        .filter(Q(can_add=True) | Q(can_change=True)).values_list('id', flat=True)
    
    q = Q()
    if global_ids:
        q = Q(globalpagepermission__id__in=global_ids)
        # haves some global permissions assigned
        if not qs.filter(q).count():
            # haves global permissions, but none of sites is specified, so he haves 
            # access to all sites 
            return qs
    
    # add some pages if he haves permission to add / change her    
    q |= Q(Q(page__pagepermission__user=user) | Q(page__pagepermission__group__user=user)) & \
        Q(Q(page__pagepermission__can_add=True) | Q(page__pagepermission__can_change=True))
    
    return qs.filter(q)
    
    