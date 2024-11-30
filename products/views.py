from django.shortcuts import redirect, render
from .models import Product
from .forms import ProductForm
from accounts.models import Profile
from django.db.models import Avg, Count

# دي الفيو بتاعت إنشاء المنتج الجديد
def create_product(request):
    # لو ال request نوعه POST يعني في فورم جاي من اليوزر
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # لو الفورم صح و مفيش مشاكل فيه
        if form.is_valid():
            # هنسيف البيانات في الداتا بيز
            product = form.save()
            # بعد ما نعمل المنتج نوديه على صفحة التفاصيل بتاعته باستخدام ال slug بتاعه
            return redirect('product_detail', slug = product.slug)
    else:
        # لو مش POST يبقى هنخلي الفورم فاضي علشان اليوزر يدخل البيانات
        form = ProductForm()
    # هنرجع الصفحة بتاعت create_product مع الفورم
    return render(request, 'create_product.html', {'form': form})

# دي الفيو بتاعت عرض تفاصيل المنتج
def product_detail(request, slug):
    # هنا هنجيب المنتج من الداتا بيز باستخدام ال slug
    product = Product.objects.get(slug=slug)
    # هنجلب اليوزر اللي هو المالك بتاع المنتج
    user = product.user
    # هنا بنجيب صورة البروفايل بتاعته من جدول البروفايل
    user_img = Profile.objects.get(user=user).ProfileImg
    # و بنجيب اسم الشركة اللي تابع ليها اليوزر
    company_name = Profile.objects.get(user=user).company_name
    # هنجيب المنتجات المتشابهة في الفئة لكن مش ده المنتج نفسه
    related_products = Product.objects.filter(catigory=product.catigory).exclude(slug=slug).annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
    # هنحسب المعدل المتوسط للتقييمات
    product_rate_avg = product.ratings.aggregate(Avg('rating'))
    # لو المعدل المتوسط مش موجود (يعني المنتج لسه مفيش تقييمات)، هنخليه 0
    if product_rate_avg['rating__avg'] is None:
        product_rate_avg['rating__avg'] = 0
    # هنجيب عدد التقييمات لكل درجة من درجات التقييم
    ratings_count = product.ratings.values('rating').annotate(count=Count('rating')).order_by('-rating')
    # هنجيب عدد الناس اللي قيموا المنتج
    number_of_rater = product.ratings.count()

    # هنا بنعرض النتيجة في الكونسول علشان نعرف لو فيه مشكلة ولا لأ
    print(range(1, int(product_rate_avg['rating__avg'])))
    
    # هنرجع صفحة التفاصيل مع كل البيانات اللي محتاجينها
    return render(request, 'product_detail.html', {'product': product, 'user_img': user_img, 'company_name': company_name,'ratings_count': ratings_count, 'related_products': related_products,'product_rate_avg': product_rate_avg, 'number_of_rater': number_of_rater,'int_avg_rate':range(0, int(product_rate_avg['rating__avg']))})
