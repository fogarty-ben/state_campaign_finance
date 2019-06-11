from django.db import models

# Create your models here.
class contributions(models.Model):
    primary_key = models.UUIDField(primary_key=True)
    committee_state = models.CharField(max_length=10, blank=True, null=True)
    trans_id = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    committee_cd = models.CharField(max_length=300, blank=True, null=True)
    committee_type = models.CharField(max_length=300, blank=True, null=True)
    committee_name = models.CharField(max_length=300, blank=True, null=True)
    trans_type = models.CharField(max_length=200, blank=True, null=True)
    trans_subtype = models.CharField(max_length=200, blank=True, null=True)
    contrib_commitee_cd = models.CharField(max_length=200, blank=True, null=True)
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
    amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financelarge'

class interested_user(models.Model):
    email = models.EmailField(max_length=254)
    interested_state = models.CharField(max_length=2)

    @classmethod
    def create(cls, email, state):
        user = cls(email=email, interested_state=state)
        return user
