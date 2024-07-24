from django.contrib import admin
from .models import TeamLeader, Associate, Project, PlotNumber, Payment, Record

@admin.register(TeamLeader)
class TeamLeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')
    search_fields = ('name',)

@admin.register(Associate)
class AssociateAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'team_leader')
    search_fields = ('name',)
    list_filter = ('team_leader',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'total_amount')
    search_fields = ('name',)
    list_filter = ('description',)

@admin.register(PlotNumber)
class PlotNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'project', 'plot_size')
    search_fields = ('number',)
    list_filter = ('project',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('record', 'amount', 'date_time', 'part')
    search_fields = ('record__client_name', 'amount')
    list_filter = ('date_time', 'part')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'project', 'plot_number', 'total_amount', 'discount', 'deal_value', 'part_a', 'part_b', 'remaining_amount')
    search_fields = ('client_name', 'project__name', 'plot_number__number')
    list_filter = ('project', 'plot_number')

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.update_remaining_amount()
