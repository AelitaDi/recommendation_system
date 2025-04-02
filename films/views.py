from django.views.generic import ListView

from films.models import Film


class FilmListView(ListView):
    model = Film
    paginate_by = 10

    def get_queryset(self):
        if not CACHE_ENABLED:
            return super().get_queryset()
        key = "products_list"
        products = cache.get(key)
        if products is not None:
            return products
        products = super().get_queryset()
        cache.set(key, products, 60 * 15)
        return products


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save(commit=False)
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModerForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("catalog.delete_product") or user == self.object.owner:
            return self.form_class
        raise PermissionDenied

    def form_valid(self, form):
        user = self.request.user
        if user.has_perm("catalog.delete_product") or user == self.object.owner:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        raise PermissionDenied