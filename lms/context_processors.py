from .models import Course, Author, Category,SiteInfo

def get_all_categories(request):
    categories = Category.objects.all()
    category_counts = []
    for category in categories:
        course_count = Course.objects.filter(category=category).count()
        if course_count > 0:  # Only include non-empty categories
            category_counts.append({'category': category, 'course_count': course_count})
    context = {
        "categories":categories,
        "category_counts": category_counts,
    }
    return context


def siteinfo(request):
    siteinfo = SiteInfo.objects.all()
    context ={
        'siteinfo': siteinfo,
    }
    return context


