from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls", namespace="accounts")),
    path("api/courses/", include("apps.courses.urls", namespace="courses")),
    path("api/cart/", include("apps.cart.urls", namespace="cart")),
    path("api/orders/", include("apps.orders.urls", namespace="orders")),
    path("api/blog/", include("apps.blog.urls", namespace="blog")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
