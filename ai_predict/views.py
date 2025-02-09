from django.shortcuts import render
from products.models import Product
from .forms import ProductForm
from .helper import recommend_products_tfidf
import pandas as pd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def predict(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            price_range = (form.cleaned_data['price_min'], form.cleaned_data['price_max'])
            
            
            products_ = Product.objects.filter(catigory=category, price__range=price_range)
            
            products_df = pd.DataFrame(list(products_.values('slug', 'title', 'catigory', 'price', 'description')))
            
            
            if not products_df.empty:
                
                recommendations = recommend_products_tfidf(products_df, description)
                
                recommendations = recommendations[['slug', 'title', 'catigory', 'price', 'similarity']]
                recommendations['similarity'] = recommendations['similarity'].apply(lambda x: round(x, 1))
                
                recommendations = recommendations.to_dict('records')
                
                recommendations = [product for product in recommendations if product['similarity'] >= 0.1]
                
                recommendations_products = Product.objects.filter(slug__in=[product['slug'] for product in recommendations])
                
                page = request.GET.get('page', 1)
                paginator = Paginator(recommendations_products, 5)
                try:
                    recommendations_products = paginator.page(page)
                except PageNotAnInteger:
                    recommendations_products = paginator.page(1)
                except EmptyPage:
                    recommendations_products = paginator.page(paginator.num_pages)

                
                return render(request, 'prediction_list.html', {'recommendations': recommendations_products})
            else:
                return render(request, 'prediction_form.html', {'error': 'No products found for the given filters.', 'form': form})
        else:
            return render(
                request,
                'prediction_form.html',
                {
                    'form': form,
                    'error': 'There were errors in the form. Please correct them.',
                    'form_errors': form.errors,  
                }
            )
    else:
        form = ProductForm()
        return render(request, 'prediction_form.html', {'form': form})
