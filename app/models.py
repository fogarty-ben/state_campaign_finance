from django.db import models

# Create your models here.
class Campaignfinance(models.Model):
    primary_key = models.UUIDField(primary_key=True)
    commitee_state = models.CharField(max_length=10, blank=True, null=True)
    trans_id = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    committee_cd = models.DecimalField(max_digits=500, decimal_places=250, blank=True, null=True)
    committee_type = models.CharField(max_length=300, blank=True, null=True)
    commitee_name = models.CharField(max_length=300, blank=True, null=True)
    trans_type = models.CharField(max_length=50, blank=True, null=True)
    trans_subtype = models.CharField(max_length=50, blank=True, null=True)
    contrib_commitee_cd = models.DecimalField(max_digits=50, decimal_places=0, blank=True, null=True)
    contrib_org = models.CharField(max_length=300, blank=True, null=True)
    contrib_full_name = models.CharField(max_length=300, blank=True, null=True)
    contrib_prefix = models.CharField(max_length=300, blank=True, null=True)
    contrib_suffix = models.CharField(max_length=300, blank=True, null=True)
    contrib_first = models.CharField(max_length=300, blank=True, null=True)
    contrib_middle = models.CharField(max_length=300, blank=True, null=True)
    contrib_last = models.CharField(max_length=300, blank=True, null=True)
    contrib_occupation = models.CharField(max_length=300, blank=True, null=True)
    contrib_employer = models.CharField(max_length=300, blank=True, null=True)
    contrib_addr_line_1 = models.CharField(max_length=500, blank=True, null=True)
    contrib_addr_line_2 = models.CharField(max_length=500, blank=True, null=True)
    contrib_city = models.CharField(max_length=500, blank=True, null=True)
    contrib_state = models.CharField(max_length=500, blank=True, null=True)
    contrib_zip = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=500, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaignfinance'