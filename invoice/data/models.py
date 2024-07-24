from django.db import models

class TeamLeader(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def get_associates(self):
        return self.associates.all()

class Associate(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    team_leader = models.ForeignKey(TeamLeader, related_name='associates', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    total_amount = models.IntegerField()

    class Meta:
        unique_together = ('name', 'description')

    def __str__(self):
        return self.name

class PlotNumber(models.Model):
    number = models.CharField(max_length=50)
    project = models.ForeignKey(Project, related_name='plot_numbers', on_delete=models.CASCADE)
    plot_size = models.FloatField()  # Added plot_size field

    def __str__(self):
        return f"{self.number} - {self.project.name} - {self.plot_size} acres"

class Payment(models.Model):
    record = models.ForeignKey('Record', related_name='payments', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    part = models.CharField(max_length=1, choices=[('A', 'Cash'), ('B', 'Cheque/Loan')])

    def __str__(self):
        return f"Payment of {self.amount} for {self.record.client_name}"

class Record(models.Model):
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, blank=True, null=True)
    associate_name = models.OneToOneField(Associate, max_length=20, blank=True, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    plot_number = models.OneToOneField(PlotNumber, blank=True, null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    total_amount = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(default=0)
    deal_value = models.IntegerField(blank=True, null=True)
    part_a = models.IntegerField(default=0)
    part_b = models.IntegerField(default=0)
    remaining_amount = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.plot_number and self.project:
            self.total_amount = self.project.total_amount * self.plot_number.plot_size
        self.deal_value = self.total_amount - self.discount
        self.remaining_amount = (self.part_a + self.part_b) - self.deal_value
        super().save(*args, **kwargs)

    def update_remaining_amount(self):
        payments = self.payments.all()
        self.part_a = sum(payment.amount for payment in payments if payment.part == 'A')
        self.part_b = sum(payment.amount for payment in payments if payment.part == 'B')
        self.remaining_amount = (self.part_a + self.part_b) - self.deal_value
        self.save()

    def __str__(self):
        return f"{self.client_name} - {self.project.name}"
