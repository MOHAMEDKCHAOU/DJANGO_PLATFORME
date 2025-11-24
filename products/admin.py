from django.contrib import admin
from .models import Product, Reservation, Review
from .models import Category
from django.core.mail import send_mail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    
admin.site.register(Category)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "time", "people", "is_confirmed")
    list_filter = ("date", "is_confirmed")
    search_fields = ("name", "email", "phone")
    actions = ["confirm_reservation"]

    def confirm_reservation(self, request, queryset):
        for reservation in queryset:
            reservation.is_confirmed = True
            reservation.save()

            # Send Confirm Email
            send_mail(
                subject="Your Table Reservation is Confirmed",
                message=f"Hello {reservation.name},\n\nYour reservation on {reservation.date} at {reservation.time} has been confirmed.\n\nThank you!",
                from_email="hamakch12@email.com",
                recipient_list=[reservation.email],
                fail_silently=False,
            )
        self.message_user(request, "Reservation(s) confirmed and email sent!")

    confirm_reservation.short_description = "Confirm reservation and send email"